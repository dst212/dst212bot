import langs
import logging
log = logging.getLogger(__name__)

import os, json, datetime, threading

from pyrogram.types import Chat, User, Message

class Option:
	def __init__(self, t: type, default, minimum=None, maximum=None, options: list=[]):
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
		self.usr = {}
		self.mutex = threading.Lock()
		self.values = {
			"lang": Option(str, "auto", options=["auto"] + langs.available()),
			"sync-tr": Option(bool, False),
			"override": Option(bool, False),
		}
		self.defauls = {k: v.default for k, v in self.values.items()}

	def save(self, uid: int, config: dict):
		self.mutex.acquire()
		try:
			os.makedirs(self.base_dir, exist_ok=True)
			with open(f"{self.base_dir}{uid}", "w") as f:
				json.dump(config, f)
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
					try:
						return json.load(f)
					except json:
						os.rename(file, file + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".corrupted")
						log.error("Couldn't read " + file + ", renamed.")
			return None
		except Exception as e:
			raise e
		finally:
			self.mutex.release()

	def do_override(self, m):
		return m.from_user and self.usr.get(m.from_user.id) and self.usr.get(m.from_user.id).get("override")

	def get_id(self, uid) -> int:
		if type(uid) == Message:
			if self.do_override(uid): # priority on overrides, of course
				return uid.from_user.id
			return uid.chat.id
		elif type(uid) == Chat or type(uid) == User:
			return uid.id
		return uid

	def get(self, uid, item=None):
		user = None
		uid = self.get_id(uid)
		if not self.usr.get(uid):
			user = self.load(uid)
			if not user:
				user = self.defaults.copy()
				self.save(uid, user)
			self.usr[uid] = user
		else:
			user = self.usr[uid]
		return (user.get(item) if item else user) if user else None

	def set(self, uid, item, value):
		uid = self.get_id(uid)
		i = self.values.get(item)
		if self.usr.get(uid) and i:
			if i.is_valid(value):
				self.usr[uid][item] = i.type(value)
				self.save(uid, self.usr[uid])
				return True
			else:
				raise ValueError(f"Type mismatch: {type(self.usr[uid][item])} and {type(value)} ({value})")
		return False

	def lang_code(self, uid):
		return self.get(uid, "lang")

	def lang_dict(self, uid):
		return langs.get(self.get(uid, "lang"))

	def lang(self, uid, s):
		# TODO: warn directly log-chats
		return langs.get(self.get(uid, "lang")).get(s) or langs.get("auto").get(s) or f"[Missing: <code>{s}</code>]"
