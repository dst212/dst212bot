from custom.log import log
from custom.misc import format_user
import os, json, datetime

from pyrogram.types import User, Message

class Config:
	def __init__(self, bot, users):
		self.__bot = bot
		self.__usr = users
		self.__base_dir = "./data/config/"
		self.__cfg = {
			"admin": [],		# can do admin stuff except adding or removing other admins
			"log": [],			# will get info about the bot operations (boot up, shutdown, errors)
			"helper": [],		# can use /reply
			"support": [],		# can see /hey reports, must be helper to reply
			"blocked": [],		# users/chats which can't use the bot
		}
		self.refresh_data()

	def refresh_data(self) -> None:
		os.makedirs(self.__base_dir, exist_ok=True)
		for k in self.__cfg:
			file = self.__base_dir + k + ".json"
			if os.path.exists(file):
				try:
					with open(file, "r") as f:
						self.__cfg[k] = json.load(f)
				except:
					os.rename(file, file + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".corrupted")
					log.error("Couldn't read " + file + ", renamed.")
			if not self.__cfg.get(k):
				with open(file, "w") as f:
					json.dump(self.__cfg[k], f)
		if len(self.__cfg["admin"]) == 0:
			log.warning("Please, manually set one or more admin for the bot in " + self.__base_dir + "admin.json")

	def get(self, what) -> list:
		return self.__cfg.get(what) or []
	def get_admins(self) -> list:
		return self.__cfg["admin"]
	def get_log_chats(self) -> list:
		return self.__cfg["log"]
	def get_support_chats(self) -> list:
		return self.__cfg["support"]
	def get_helpers(self) -> list:
		return self.__cfg["support"]
	def get_blocked(self) -> list:
		return self.__cfg["blocked"]

	def is_in(self, who, where) -> bool:
		if type(who) != int:
			if type(who) == Message:
				if not who.from_user:
					return False
				who = who.from_user.id
			elif type(who) == User:
				who = who.id
			else:
				return False
		if type(where) == str:
			return who in self.__cfg.get(where)
		for group in where:
			if who in self.__cfg.get(group):
				return True
		return False
		# else: True in (who in self.__cfg.get(i) for i in where)
	def is_admin(self, who) -> bool:
		return self.is_in(who, "admin")
	def is_helper(self, who) -> bool:
		return self.is_in(who, ["admin", "helper"])
	def is_blocked(self, who) -> bool:
		return self.is_in(who, "blocked")

	def get_users_groups(self, l) -> list:
		out = []
		for i in l:
			try: out += [self.__bot.get_users(i)]
			except:
				try: out += [self.__bot.get_chat(i)]
				except: pass
		return out
	def list_all(self, l) -> str:
		out = []
		for i in l:
			try: res = self.__bot.get_users(i)
			except:
				try: res = self.__bot.get_chat(i)
				except: pass
			out += [format_user(res) if res else f"[<code>{i}</code>] (dead)"]
		return ", ".join(out)

	def add_items(self, group, ids) -> str:
		if group not in self.__cfg or group == "admin":
			return "<code>{group}</code> is not a valid group."
		out = ""
		for item in self.get_users_groups(ids):
			out += format_user(item)
			if item.id in self.__cfg[group]:
				out += f" already in <code>{group}</code>.\n"
			else:
				self.__cfg[group] += [item.id]
				out += f" added to <code>{group}</code>.\n"
		with open(self.__base_dir + group + ".json", "w") as f:
			json.dump(self.__cfg[group], f)
			out += "\nConfig updated."
		return out
	def rem_items(self, group, ids) -> str:
		if group not in self.__cfg or group == "admin":
			return "<code>{group}</code> is not a valid group."
		out = ""
		for item in self.get_users_groups(ids):
			out += format_user(item)
			if item.id in self.__cfg[group]:
				self.__cfg[group].remove(item.id)
				out += f" removed from <code>{group}</code>.\n"
			else:
				out += f" is not in <code>{group}</code>.\n"
		with open(self.__base_dir + group + ".json", "w") as f:
			json.dump(self.__cfg[group], f)
			out += "\nConfig updated."
		return out
