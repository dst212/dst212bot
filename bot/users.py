import langs

import datetime, googletrans, json, logging, os, threading
log = logging.getLogger(__name__)

from pyrogram.types import Chat, User, Message, CallbackQuery, InlineQuery
from pyrogram.enums import ChatType, ChatAction
import pyrogram.errors as Errors

class Option:
	def __init__(self, t: type, default, minimum=None, maximum=None, options: dict={}):
		self.type = t
		self.default = default
		self.min = minimum
		self.max = maximum
		self.options = options

	def is_valid(self, value):
		try:
			value = self.type(value)
		except:
			return False
		return self.type == bool or (value in self.options if self.options else self.min <= value <= self.max)

class Users:
	def __init__(self, bot):
		self.base_dir = "./data/users/"
		self.unused_dir = "./data/deactivated/"
		self.bot = bot
		self.chat = {}
		self.mutex = threading.Lock()
		self.values = {
			"lang": Option(str, "auto", options={i: f"{langs.flag(i)}{langs.formal_name(i)}" for i in ["auto"] + langs.available()}),
			"auto-tr": Option(str, "off", options={k: v for i in [{"off": "OFF", "auto": "AUTO"}, {k: f"{k} ({v})" for k, v in googletrans.LANGUAGES.items()}] for k, v in i.items()}),
			"override": Option(bool, False),
			"fwd": Option(bool, False),
		}
		self.default = {k: v.default for k, v in self.values.items()}

	def save(self, uid: int, config: dict=None):
		self.mutex.acquire()
		try:
			os.makedirs(self.base_dir, exist_ok=True)
			with open(f"{self.base_dir}{uid}", "w") as f:
				json.dump(config or self.default, f)
		except Exception as e:
			raise e
		finally:
			self.mutex.release()

	def load(self, uid: int) -> dict:
		self.mutex.acquire()
		try:
			file = f"{self.base_dir}{uid}"
			# check if the user was previously deactivated
			if not os.path.exists(file):
				unused = f"{self.unused_dir}{uid}"
				if os.path.exists(unused):
					os.rename(unused, file)
			if os.path.exists(file):
				with open(file, "r") as f:
					return json.load(f)
		except json:
			os.rename(file, file + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".corrupted")
			log.error("Couldn't read " + file + ", renamed.")
		except Exception as e:
			raise e
		finally:
			self.mutex.release()
		return None

	def forget(self, uid: int):
		self.mutex.acquire()
		try:
			file = f"{self.base_dir}{uid}"
			if os.path.exists(file):
				log.info(f"Removing settings for {uid}...")
				os.remove(file)
				if self.chat.get(uid):
					log.info(f"Removing {self.chat[uid]}...")
					del self.chat[uid]
				log.info(f"Successfully erased settings for {uid}.")
				return True
		except Exception as e:
			raise e
		finally:
			self.mutex.release()
		return False

	# move settings away from the main folder
	# settings will be re-activated if the user/chat interacts again with the bot
	def deactivate(self, uid: int):
		uid = self.get_id(uid)
		self.mutex.acquire()
		try:
			os.makedirs(self.unused_dir, exist_ok=True)
			file = f"{self.base_dir}{uid}"
			log.info(f"Deactivating settings for {uid}...")
			if os.path.exists(file):
				os.rename(file, f"{self.unused_dir}{uid}")
				if self.chat.get(uid):
					del self.chat[uid]
				log.info(f"Successfully deactivated settings for {uid}.")
			else:
				log.info(f"{file} not found.")
			return True
		except Exception as e:
			raise e
		finally:
			self.mutex.release()
		return False


	def do_override(self, m) -> bool:
		# it's safe to call directly self.get() here
		# it handles the creation of the user's settings if they don't exist
		return m.from_user and self.get(m.from_user.id, "override")

	# retrieve user/group id considering the "override" flag
	def get_id(self, uid) -> int:
		if type(uid) == Message:
			return uid.from_user.id if self.do_override(uid) else uid.chat.id
		elif type(uid) == CallbackQuery:
			return uid.from_user.id if self.do_override(uid) or not uid.message else uid.message.chat.id
		elif type (uid) == InlineQuery:
			return uid.from_user.id
		elif type(uid) in (Chat, User):
			return uid.id
		return uid

	# get chat's settings or values
	def get(self, uid, item=None):
		user = None
		uid = self.get_id(uid)
		if not self.chat.get(uid):
			log.info(f"Loading settings for {uid}...")
			user = self.load(uid)
			if not user:
				log.info(f"{uid} not found in files, creating...")
				user = self.default.copy()
				self.save(uid, user)
			self.chat[uid] = user
			log.info(f"Loaded settings for {uid}: {user}")
		else:
			user = self.chat[uid]
		# add the option if it wasn't written yet, then save it
		if item:
			if not self.values.get(item):
				return None
			elif user.get(item) is None:
				user[item] = self.values[item].default
				self.save(uid, user)
		return (user.get(item) if item else user) if user else None

	# modify chat's settings
	def set(self, uid, item, value):
		uid = self.get_id(uid)
		i = self.values.get(item)
		if self.chat.get(uid) and i:
			if i.is_valid(value):
				self.chat[uid][item] = i.type(value)
				self.save(uid, self.chat[uid])
				return True
			else:
				raise ValueError(f"Type mismatch: {type(self.chat[uid][item])} and {type(value)} ({value})")
		return False

	# the user is valid, didn't stop the bot and wasn't deleted
	def can_send_to(self, uid: int) -> bool:
		if uid:
			try:
				self.bot.send_chat_action(uid, ChatAction.TYPING)
				self.bot.send_chat_action(uid, ChatAction.CANCEL)
				return True
			except (Errors.UserIsBlocked, Errors.InputUserDeactivated) as e:
				log.info(f"Deactivating [{uid}]: {e}")
				self.deactivate(uid)
			except Errors.UserIdInvalid:
				log.info(f"[{i}] is an invalid id. Forgetting it.")
				self.forget(i)
			except Errors.PeerIdInvalid:
				log.info(f"[{uid}] has never interacted with the bot privately.")
			except Exception as e:
				log.warning(f"[{uid}]: {e}")
		return False

	# retrieve all chats' ids for which settings were saved
	def get_all_chats(self):
		chats = []
		for i in os.listdir(self.basr_dir):
			try:
				chats.append(int(i))
			except:
				pass
		return chats

	# retrieve active chats list
	def get_active_chats_list(self):
		return self.get_active_chats(as_list=True)

	# retrieve active chats grouped by chat type
	def get_active_chats(self, as_list=False):
		chats = [] if as_list else {k.name: {} for k in ChatType}
		add = (lambda chat : chats.append(chat)) if as_list else (lambda chat : chats[chat.type.name].update({chat.id: chat}))
		for i in os.listdir(self.base_dir):
			try:
				chat = self.bot.get_chat(int(i))
				if type(chat) != Chat:
					log.warning(f"Settings for {i} are unused. Deactivating.")
					self.deactivate(i)
				elif self.can_send_to(chat.id):
					add(chat)
			except (Errors.ChannelInvalid, Errors.ChannelPrivate) as e:
				log.warn(f"Channel {i} is private or invalid. Deactivating it.")
				self.deactivate(i)
			except Errors.UserIdInvalid:
				log.warn(f"[{i}] is an invalid id. Forgetting it.")
				self.forget(i)
			except Errors.PeerIdInvalid:
				# log.warn(f"Chat {i} never interacted with the bot.")
				pass
			except Exception as e:
				log.warning(f"[{uid}]: {e}")
		if not as_list:
			chats["count"] = sum([len(i) for i in chats.values()])
		return chats

	# enable/disable/get chat-forward
	def enable_forward(self, uid):
		return self.set(uid, "fwd", True)
	def disable_forward(self, uid):
		return self.set(uid, "fwd", False)
	def do_forward(self, uid):
		return self.get(uid, "fwd")

	# messages and queries can (and should) be passed as uid, they will be parsed later on in get_id()
	def lang_code(self, uid):
		lang = self.get(uid, "lang")
		# uses user's language code (provided by pyrogram) if the language is "auto"
		if lang != "auto":
			return lang
		user = None
		uid = self.get_id(uid)
		try:
			user = self.bot.get_users(uid) if uid > 0 else None
		except Exception as e:
			log.warning(f"User {uid} not found, using English")
		return user.language_code if user else "en"

	def lang_dict(self, uid):
		return langs.get(self.get(uid, "lang"))

	def lang(self, uid, s):
		return langs.get(self.get(uid, "lang")).get(s)
