import langs

import datetime, googletrans, json, logging, os, threading
log = logging.getLogger(__name__)

from pyrogram.types import Chat, User, Message, CallbackQuery, InlineQuery
from pyrogram.enums import ChatType

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

	# retrieve all chats' ids for which settings were saved
	def get_all_chats():
		chats = []
		for i in os.listdir(self.basr_dir):
			try:
				chats.append(int(i))
			except:
				pass
		return chats

	# retrieve active chats list
	def get_active_chats_list(self):
		chats = []
		for i in os.listdir(self.base_dir):
			try:
				i = self.bot.get_chat(int(i))
				if type(i) == Chat:
					chats.append(i)
			except:
				pass
		return chats

	# retrieve active chats grouped in objects
	def get_active_chats(self):
		chats = {}
		count = 0
		for i in os.listdir(self.base_dir):
			try:
				i = self.bot.get_chat(int(i))
				if type(i) == Chat:
					if not chats.get(i.type.name):
						chats[i.type.name] = {}
					chats[i.type.name][i.id] = i
					count += 1
			except:
				pass
		# this is actually useless as one could simply do something like
		# len(chats["BOT"]) which is also shorter to type than chats["BOT"]["count"] 
		# for v in chats.values():
		# 	v["count"] = len(v)
		# 	count += len(v) # obviously if this is on, count += 1 (some lines above) must be removed
		chats["count"] = count
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
