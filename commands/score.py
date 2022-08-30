import json, html, os, re

class Score:
	def __init__(self, users):
		self.__usr = users
		self.__base_dir = "data/score/"

	def sort(self, data):
		data["items"] = {k: v for k, v in sorted(data["items"].items(), key=lambda x: x[1], reverse=True)}

	def score_str(self, LANG, score):
		return f"<b>{html.escape(score['display'])}</b>\n\n" + (("\n".join(f"<i>{html.escape(k)}</i> : <code>{v}</code>" for k, v in score["items"].items()) or LANG('SCORE_NO_ITEMS')))

	def get_score(self, LANG, m, name):
		cdir = f"{self.__base_dir}{m.chat.id}/"# + message.from_user.id
		os.makedirs(cdir, exist_ok=True)
		if not bool(re.match("^[a-zA-Z0-9_-]+$", name)):
			m.reply(LANG('SCORE_INVALID_NAME'))
			return ""
		return cdir + name + ".json"

	def score_get(self, LANG, m, score):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return
		data = {}
		with open(file, "r") as f:
			data = json.load(f)
		m.reply(self.score_str(LANG, data))

	def score_new(self, LANG, m, score):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if os.path.exists(file):
			m.reply(LANG('SCORE_ALREADY_EXISTS').format(score))
			return
		data = {
			"display": score,
			"owner": m.from_user.id,
			"editors": [m.from_user.id],
			"items": {},
		}
		with open(file, "w") as f:
			json.dump(data, f)
		m.reply(LANG('SCORE_CREATED_SUCCESSFULLY').format(score))

	def score_del(self, LANG, m, score):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return
		data = {}
		with open(file, "r") as f:
			data = json.load(f)
			if not m.from_user.id == data["owner"]:
				m.reply(LANG('SCORE_YOU_ARENT_THE_OWNER'))
				return
		os.remove(file)
		m.reply(LANG('SCORE_WAS_NOW_GONE').format(self.score_str(LANG, data)))

	def score_add(self, LANG, m, score, item, value=1):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return
		data = {}
		with open(file) as f:
			data = json.load(f)
			if not m.from_user.id in data["editors"]:
				m.reply(LANG('SCORE_YOU_ARENT_AN_EDITOR'))
				return
		if not data["items"].get(item):
			data["items"][item] = 0
		data["items"][item] += value
		self.sort(data)
		with open(file, "w") as f:
			json.dump(data, f)
		m.reply(LANG('SCORE_ITEM_SET_TO').format(html.escape(item), html.escape(data["display"]), data["items"][item]))

	def score_set(self, LANG, m, score, item, value=1):
		file = self.get_score(LANG, m, score)
		if not file:
			return False
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return False
		data = {}
		with open(file) as f:
			data = json.load(f)
			if not m.from_user.id in data["editors"]:
				m.reply(LANG('SCORE_YOU_ARENT_AN_EDITOR'))
				return False
		if data["items"].get(item) and value == 0:
			del data["items"][item]
		elif value != 0:
			data["items"][item] = value
			self.sort(data)
		with open(file, "w") as f:
			json.dump(data, f)
		if value != 0:
			m.reply(LANG('SCORE_ITEM_SET_TO').format(html.escape(item), html.escape(data["display"]), data["items"][item]))
		else:
			m.reply(LANG('SCORE_ITEM_DELETED').format(html.escape(item), html.escape(data["display"])))
		return True

	def score_ren(self, LANG, m, score, newname):
		file = self.get_score(LANG, m, score)
		newfile = self.get_score(LANG, m, newname)
		if not file or not newfile:
			return
		with open(file, "r") as f:
			data = json.load(f)
			if not m.from_user.id == data["owner"]:
				m.reply(LANG('SCORE_YOU_ARENT_THE_OWNER'))
				return
		os.rename(file, newfile)
		m.reply(LANG('SCORE_RENAMED_FROM').format(score, newname))

	def score_display(self, LANG, m, score, display):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return
		data = {}
		with open(file, "r") as f:
			data = json.load(f)
		if not m.from_user.id == data["owner"]:
			m.reply(LANG('SCORE_YOU_ARENT_THE_OWNER'))
			return
		data["display"] = display
		with open(file, "w") as f:
			json.dump(data, f)
		m.reply(LANG('SCORE_DISPLAY_SET').format(score, display))

	def score_setraw(self, LANG, m, score, items):
		file = self.get_score(LANG, m, score)
		if not file:
			return
		if not os.path.exists(file):
			m.reply(LANG('SCORE_DOESNT_EXIST').format(score))
			return
		data = {}
		with open(file, "r") as f:
			data = json.load(f)
		if not m.from_user.id == data["owner"]:
			m.reply(LANG('SCORE_YOU_ARENT_THE_OWNER'))
			return
		was = self.score_str(LANG, data)
		data["items"] = items
		with open(file, "w") as f:
			json.dump(data, f)
		m.reply(f"{LANG('SCORE_WAS').format(was)}\n\n{LANG('SCORE_NOW_ITS').format(self.score_str(LANG, data))}")

	def command(self, LANG, bot, message):
		args = (message.text or message.caption).split(" ")
		if len(args) > 1:
			if args[1] in ("h", "help"):
				message.reply(LANG('SCORE_HELP'))
			elif args[1] in ("get", "print"):
				if len(args) <= 2:
					message.reply(LANG('SCORE_PROVIDE_NAME'))
					return
				elif len(args) > 3:
					message.reply(LANG('SCORE_UNNEEDED_ARGUMENT'))
					return
				self.score_get(LANG, message, args[2])
			elif args[1] in ("new", "create"):
				if len(args) <= 2:
					message.reply(LANG('SCORE_PROVIDE_NAME'))
					return
				elif len(args) > 3:
					message.reply(LANG('SCORE_UNNEEDED_ARGUMENT'))
					return
				self.score_new(LANG, message, args[2])
			elif args[1] in ("del", "delete", "remove"):
				if len(args) <= 2:
					message.reply(LANG('SCORE_PROVIDE_NAME'))
					return
				for arg in args[2:]:
					self.score_del(LANG, message, arg)
			elif args[1] in ("ren", "rename"):
				if len(args) <= 3:
					message.reply(LANG('SCORE_PROVIDE_NAME'))
					return
				self.score_ren(LANG, message, args[2], args[3])
			elif args[1] in ("display", "setdisplay"):
				if len(args) <= 3:
					message.reply(LANG('SCORE_PROVIDE_NAME'))
					return
				self.score_display(LANG, message, args[2], " ".join(args[3:]))
			elif args[1] in ("add",):
				if len(args) <= 3:
					message.reply(LANG('USAGE') + ":\n<code>/score add score_name item_name [value=1]</code>\n\nIncrement by <code>value</code> the item <code>item_name</code> of <code>score_name</code>.\nYou may use negative values as <code>value</code>.")
					return
				try:
					self.score_add(LANG, message, args[2], args[3], int(args[4]) if len(args) > 4 else 1)
				except ValueError:
					m.reply(LANG('SCORE_ONLY_NUMBERS'))
			elif args[1] in ("set",):
				if len(args) <= 3:
					message.reply(LANG('USAGE') + ":\n<code>/score set score_name item_name [value=1]</code>\n\nSet to <code>value</code> the item <code>item_name</code> of <code>score_name</code>.")
					return
				try:
					self.score_set(LANG, message, args[2], args[3], int(args[4]) if len(args) > 4 else 1)
				except ValueError:
					message.reply(LANG('SCORE_ONLY_NUMBERS'))
			elif args[1] in ("setraw",):
				i = args[2].find("\n") if len(args) > 2 else -1
				if i == -1:
					message.reply(LANG('USAGE') + ":\n<code>/score setraw score_name\nitem1 : value\nitem2 : value\nitem3 : value</code>\n\nFor each new line, create a item and assign the specified value to it.")
					return
				score = args[2][:i]
				items = {}
				try:
					for item in (message.text or message.caption).split("\n")[1:]:
						item = item.split(":")
						if len(item) > 0 and item[0] != "":
							items[item[0].strip()] = int(item[1]) if len(item) > 1 else 1
				except ValueError:
					message.reply(LANG('SCORE_ONLY_NUMBERS'))
				self.score_setraw(LANG, message, score, items)
			elif args[1] in ("delitem",):
				if len(args) <= 3:
					message.reply(LANG('SCORE_PROVIDE_ITEM_NAME'))
					return
				self.score_set(LANG, message, args[2], args[3], 0)
			else:
				message.reply(LANG('INVALID_SYNTAX'))
		else:
			message.reply(LANG('SCORE_HELP'))
				