import logging
log = logging.getLogger(__name__)

from custom.misc import format_user
import os, json, datetime

from pyrogram.types import User, Message

class Config:
	def __init__(self, bot, users):
		self.bot = bot
		self.usr = users
		self.file = "data/config.json"
		self.default = {
			"admin": [],		# can do admin stuff except adding or removing other admins
			"log": [],			# will get info about the bot operations (boot up, shutdown, errors)
			"support": [],		# can see /hey reports
			"helper": [],		# can reply to /hey reports (also admin can do that whether they're helper or not)
			"blocked": [],		# users/chats which can't use the bot
		}
		self.cfg = self.default.copy()
		self.reload()

	def reload(self) -> None:
		if os.path.exists(self.file):
			obj = {}
			try:
				with open(self.file, "r") as f:
					obj = json.load(f)
			except e:
				log.error(e)
				os.rename(self.file, self.file + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".corrupted")
				log.error(f"Couldn't correctly read and parse {self.file}, renamed.")
			# add loaded groups to current config
			for k, v in obj.items():
				self.cfg[k] = v
		else:
			with open(self.file, "w") as f:
				json.dump(self.cfg, f, indent=2)
		if len(self.cfg["admin"]) == 0:
			log.warning(f"No admins listed in {self.file}, add one or more. See https://github.com/dst212/dst212bot/blob/main/README.md#configuration for further details.")

	def get(self, what) -> list:
		return self.cfg.get(what) or []
	def get_admins(self) -> list:
		return self.cfg["admin"]
	def get_log_chats(self) -> list:
		return self.cfg["log"]
	def get_support_chats(self) -> list:
		return self.cfg["support"]
	def get_helpers(self) -> list:
		return self.cfg["helper"]
	def get_blocked(self) -> list:
		return self.cfg["blocked"]

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
			return who in self.cfg.get(where)
		for group in where:
			if who in self.cfg.get(group):
				return True
		return False
		# else: True in (who in self.cfg.get(i) for i in where)
	def is_admin(self, who) -> bool:
		return self.is_in(who, "admin")
	def is_helper(self, who) -> bool:
		return self.is_in(who, ["admin", "helper"])
	def is_blocked(self, who) -> bool:
		return self.is_in(who, "blocked")

	def get_users_groups(self, l) -> list:
		out = []
		for i in l:
			try: out += [self.bot.get_users(i)]
			except:
				try: out += [self.bot.get_chat(i)]
				except: pass
		return out
	def list_all(self, l) -> str:
		out = []
		for i in l:
			res = None
			try: res = self.bot.get_users(i)
			except:
				try: res = self.bot.get_chat(i)
				except: pass
			out += [format_user(res) if res else f"[<code>{i}</code>] (dead)"]
		return ", ".join(out)

	def add_items(self, LANG, group, ids) -> str:
		if group not in self.cfg or group == "admin":
			return LANG('CONFIG_IS_NOT_A_VALID_GROUP').format(group)
		out = ""
		for item in self.get_users_groups(ids):
			if item.id in self.cfg[group]:
				out = LANG('CONFIG_ALREADY_IN').format(format_user(item), group) + "\n"
			else:
				self.cfg[group] += [item.id]
				out = LANG('CONFIG_ADDED_TO').format(format_user(item), group) + "\n"
		with open(self.base_dir + group + ".json", "w") as f:
			json.dump(self.cfg[group], f)
			out = (out or LANG('NOTHING_CHANGED')) + "\n" + LANG('CONFIG_UPDATED')
		return out
	def rem_items(self, LANG, group, ids) -> str:
		if group not in self.cfg or group == "admin":
			return LANG('CONFIG_IS_NOT_A_VALID_GROUP').format(group)
		out = ""
		for item in self.get_users_groups(ids):
			if item.id in self.cfg[group]:
				self.cfg[group].remove(item.id)
				out = LANG('CONFIG_REMOVED_FROM').format(format_user(item), group) + "\n"
			else:
				out = LANG('CONFIG_NOT_IN').format(format_user(item), group) + "\n"
		with open(self.base_dir + group + ".json", "w") as f:
			json.dump(self.cfg[group], f)
			out = (out or LANG('NOTHING_CHANGED')) + "\n" + LANG('CONFIG_UPDATED')
		return out

	def log(self, text: str, forward: list[Message]=[], exclude: list=[]):
		for a in self.get_log_chats():
			if a not in exclude:
				try:
					self.bot.send_message(a, text)
					for m in forward:
						m.forward(a)
				except Exception as e:
					log.error(f"[{a}] {e}")
