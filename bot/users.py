import langs
from custom.log import log
import os, json, datetime

from pyrogram.types import Chat, User, Message

class Users:
	def __init__(self, bot):
		self.__base_dir = "./data/users/"
		self.__bot = bot
		self.__usr = {}

	def save(self, uid: int, config: dict):
		os.makedirs(self.__base_dir, exist_ok=True)
		with open(f"{self.__base_dir}{uid}", "w") as f:
			json.dump(config, f)

	def load(self, uid: int) -> dict:
		file = f"{self.__base_dir}{uid}"
		if os.path.exists(file):
			with open(file, "r") as f:
				try:
					return json.load(f)
				except json:
					os.rename(file, file + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".corrupted")
					log.error("Couldn't read " + file + ", renamed.")
		return None

	def do_override(self, m):
		return m.from_user and self.__usr.get(m.from_user.id) and self.__usr.get(m.from_user.id).get("override")

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
		if not self.__usr.get(uid):
			user = self.load(uid)
			if not user:
				user = {
					"lang": "auto",		# default language
					"sync-tr": False,	# sync default language with /translate
					"override": False	# override group settings
				}
				self.save(uid, user)
			self.__usr[uid] = user
		else:
			user = self.__usr[uid]
		return (user.get(item) if item else user) if user else None

	def lang_code(self, uid):
		return self.get(uid, "lang")

	def lang_dict(self, uid):
		return langs.get(self.get(uid, "lang"))

	def lang(self, uid, s):
		# TODO: warn directly log-chats
		return langs.get(self.get(uid, "lang")).get(s) or langs.get("auto").get(s) or f"[Missing: <code>{s}</code>]"
