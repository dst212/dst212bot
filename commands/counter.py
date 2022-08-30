from custom.log import log
import json, html, os, re, threading

class Counter:
	def __init__(self, users):
		self.__usr = users
		self.__base_dir = "./data/counter/"
		self.__groups = {}
		self.__mutex = threading.Lock()
		threading.Thread(target=self.load_all).start()

	def is_valid_name(self, name: str) -> bool:
		return bool(re.match("^[a-zA-Z0-9_-]+$", name))

	def update_group(self, chat, counter, data):
		g = self.__groups.get(chat)
		if g and g.get(counter):
			g[counter] = data

	def save(self, chat, counter, data) -> bool:
		if self.is_valid_name(counter):
			cd = f"{self.__base_dir}{chat}/"
			os.makedirs(cd, exist_ok=True)
			with open(cd + counter, "w") as f:
				json.dump(data, f)
			return True
		return False

	def load(self, chat, counter) -> dict:
		ret = None
		cd = f"{self.__base_dir}{chat}/"
		if self.is_valid_name(counter) and os.path.exists(cd + counter):
			with open(cd + counter, "r") as f:
				ret = json.load(f)
			if ret["triggers"]:
				log.info(f"Counter loaded: {counter}")
				if not self.__groups.get(chat):
					self.__groups[chat] = {}
				self.__groups[chat][counter] = ret
		return ret

	def load_all(self):
		self.__mutex.acquire()
		os.makedirs(self.__base_dir, exist_ok=True)
		for chat in os.listdir(self.__base_dir):
			for counter in os.listdir(self.__base_dir + chat):
				self.load(chat, counter)
		self.__mutex.release()

	def get(self, m, counter):
		data = self.load(str(m.chat.id), counter)
		m.reply(self.__usr.lang(m, 'COUNTER_IS').format(html.escape(data["display"]), data["value"]) if data else self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))

	def parse_message(self, m):
		text = m.text or m.caption
		if text:
			text = text.lower()
			self.__mutex.acquire()
			group = self.__groups.get(str(m.chat.id))
			if group: # log.info("COUNTER group exists")
				for k, v in group.items():
					saved = True
					for word in v["triggers"]: # log.info(f"FOR {word}")
						if word in text:
							saved = False
							self.__groups[str(m.chat.id)][k]["value"] += v["step"]
							m.reply(self.__usr.lang(m, 'COUNTER_SET').format(html.escape(v["display"]), v["value"]))
					if not saved:
						self.save(str(m.chat.id), k, v)
			self.__mutex.release()
		
	def new(self, m, counter):
		if os.path.exists(f"{self.__base_dir}{str(m.chat.id)}/{counter}"):
			m.reply(self.__usr.lang(m, 'COUNTER_ALREADY_EXISTS'))
		elif not self.save(str(m.chat.id), counter, {
			"display": counter,
			"owner": m.from_user.id,
			"editors": [m.from_user.id],
			"triggers": [],
			"value": 0,
			"step": 1,
		}):
			m.reply(self.__usr.lang(m, 'COUNTER_COULDNT_CREATE'))
		else:
			m.reply(self.__usr.lang(m, 'COUNTER_CREATED'))

	def rem(self, m, counter):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id != data["owner"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_THE_OWNER'))
		else:
			os.remove(f'{self.__base_dir}{str(m.chat.id)}/{counter}')
			group = self.__groups.get(str(m.chat.id))
			if group and group.get(counter):
				del group[counter]
			m.reply(self.__usr.lang(m, 'COUNTER_DELETED').format(html.escape(data["display"]), data["value"]))

	def set(self, m, counter, value=None, add=False):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id not in data["editors"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_AN_EDITOR'))
		else:
			if add:
				data["value"] += value if type(value) == int else data["step"]
			elif type(value) == int:
				data["value"] = value
			self.save(str(m.chat.id), counter, data)
			self.update_group(str(m.chat.id), counter, data)
			m.reply(self.__usr.lang(m, 'COUNTER_SET').format(html.escape(data["display"]), data["value"]))

	def ren(self, m, counter, newname):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id != data["owner"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_THE_OWNER'))
		else:
			path = f'{self.__base_dir}+{str(m.chat.id)}/'
			os.rename(path+counter, path+newname)
			group = self.__groups.get(str(m.chat.id))
			if group and group.get(counter):
				group[newname] = group[counter]
				del group[counter]["value"]
			m.reply(self.__usr.lang(m, 'COUNTER_RENAMED_FROM').format(counter, newname))

	def display(self, m, counter, display):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id != data["owner"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_THE_OWNER'))
		else:
			data["display"] = display
			self.update_group(str(m.chat.id), counter, data)
			m.reply(self.__usr.lang(m, 'COUNTER_DISPLAY_SET').format(counter, html.escape(display)))

	def auto_add(self, m, counter, word):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id not in data["editors"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_AN_EDITOR'))
		else:
			word = word.lower()
			data["triggers"] += [word]
			self.save(str(m.chat.id), counter, data)
			group = self.__groups.get(str(m.chat.id))
			if not group: group = self.__groups[str(m.chat.id)] = {}
			group[counter] = data
			m.reply(self.__usr.lang(m, 'COUNTER_AUTO_HAS').format(html.escape(data["display"]), html.escape(", ".join(data["triggers"]) or self.__usr.lang(m, 'COUNTER_NO_TRIGGERS'))))

	def auto_del(self, m, counter, word):
		data = self.load(str(m.chat.id), counter)
		if not data:
			m.reply(self.__usr.lang(m, 'COUNTER_DOESNT_EXIST').format(counter))
		elif not m.from_user or m.from_user.id not in data["editors"]:
			m.reply(self.__usr.lang(m, 'COUNTER_YOU_ARENT_AN_EDITOR'))
		else:
			try:
				data["triggers"].remove(word)
				self.save(str(m.chat.id), counter, data)
				if len(data["triggers"]) == 0:
					del self.__groups[str(m.chat.id)][counter]
				else:
					self.update_group(str(m.chat.id), counter, data)
				m.reply(self.__usr.lang(m, 'COUNTER_AUTO_HAS').format(html.escape(data["display"]), html.escape(", ".join(data["triggers"]))))
			except:
				m.reply(self.__usr.lang(m, 'COUNTER_WORD_NOT_FOUND').format(word, html.escape(", ".join(data["triggers"]) or self.__usr.lang(m, 'COUNTER_NO_TRIGGERS'))))

	def command(self, LANG, bot, m):
		self.__mutex.acquire()
		try:
			args = (m.text or m.caption).split(" ")
			if len(args) > 1:
				if args[1] in ("h", "help"):
					m.reply(LANG('COUNTER_HELP'))
				elif args[1] in ("get", "print"):
					if len(args) <= 2:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					self.get(m, args[2])
				elif args[1] in ("new", "create"):
					if len(args) <= 2:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					elif len(args) > 3:
						m.reply(LANG('UNNEEDED_ARGUMENT'))
						return
					self.new(m, args[2])
				elif args[1] in ("del", "delete", "remove"):
					if len(args) <= 2:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					for arg in args[2:]:
						self.rem(m, arg)
				elif args[1] in ("ren", "rename"):
					if len(args) <= 3:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					self.ren(m, args[2], args[3])
				elif args[1] in ("display", "setdisplay"):
					if len(args) <= 3:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					self.display(m, args[2], " ".join(args[3:]))
				elif args[1] in ("add",):
					if len(args) <= 2:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					try:
						self.set(m, args[2], int(args[3]) if len(args) > 3 else None, add=True)
					except ValueError:
						m.reply(LANG('COUNTER_ONLY_NUMBERS'))
				elif args[1] in ("set",):
					if len(args) <= 2:
						m.reply(LANG('COUNTER_PROVIDE_NAME'))
						return
					try:
						self.set(m, args[2], int(args[3]) if len(args) > 3 else None)
					except ValueError:
						m.reply(LANG('COUNTER_ONLY_NUMBERS'))
				elif args[1] in ("auto",):
					if len(args) <= 4:
						m.reply(LANG('INVALID_SYNTAX'))
						return
					if args[2] in ("add",):
						self.auto_add(m, args[3], " ".join(args[4:]))
					elif args[2] in ("del", "delete", "remove"):
						self.auto_del(m, args[3], " ".join(args[4:]))
				else:
					m.reply(LANG('INVALID_SYNTAX'))
			else:
				m.reply(LANG('COUNTER_HELP'))
		except Exception as e:
			raise e
		finally:
			self.__mutex.release()