from custom.log import log
from langs import Lang
import traceback, html
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class Handlers:
	def __init__(self, users, config, commands):
		self.__cfg = config
		self.__usr = users
		self.__cmds = commands
		self.__cmds.map["repeat"] = self.repeat

	def repeat(self, LANG, bot, m):
		if m.reply_to_message:
			if self.__cfg.is_admin(m) or (m.from_user and m.reply_to_message.from_user and m.from_user.id == m.reply_to_message.from_user.id):
				self.handle_update(bot, m.reply_to_message)
			else:
				m.reply_text(LANG('YOU_HAVE_NO_PERMISSIONS'))
		else:
			m.reply_text("Repeat what?")

	def handle_update(self, bot, m):
		if self.__cfg.is_blocked(m):
			#ignore the message but parse it
			self.__cmds.counter.parse_message(m)
			return
		text = m.text or m.caption
		if text:
			# make emojis valid
			text = text.encode("utf-8").decode("utf-8")
		# allow commands only from non-anonymous users, if the message is not send from helpers in a support chat
		if not self.__cmds.hey_admins.parse(bot, m) and m.from_user and text and text[0] == "/":
			LANG = Lang(self.__usr.lang_code(m)).string
			try:
				# run command
				i = text.find(" ")
				cmd = text[1:] if i == -1 else text[1:i]
				i = cmd.find("-")
				if i != -1: cmd = cmd[:i]
				i = cmd.find("@")
				if i != -1: cmd = cmd[:i] if bot.get_users("me").username == cmd[i+1:] else ""
				if self.__cmds.map.get(cmd): self.__cmds.map[cmd](LANG, bot, m)
			except Exception as e:
				traceback.print_exc()
				sender = (f"{m.from_user.mention()}, <code>{m.from_user.id}</code>" + (f" at <code>{m.chat.id}</code>" if m.chat.id != m.from_user.id else "")) if m.from_user else "Unknown"
				for a in self.__cfg.get_log_chats():
					bot.send_message(a, f"<code>#{m.chat.id}</code><code>#{m.id}#</code>\nAn exception occurred to someone ({sender}):\n\n<code>{html.escape(traceback.format_exc())}</code>\n\nMessage:")
					bot.forward_messages(a, m.chat.id, m.id)
				m.reply_text(LANG('AN_ERROR_OCCURRED_WHILE_PERFORMING'))
		else:
			self.__cmds.counter.parse_message(m)

	def handle_callback(self, bot, query):
		if self.__cfg.is_blocked(query): return # ignore the query
		try:
			LANG = Lang(self.__usr.lang_code(query.from_user)).string
			data = query.data.split(".")
			if data[0] == "help":
				self.__cmds.base.help_buttons(LANG, bot, int(data[1]), int(data[2]), [] if data[3] == "/" else [data[3]])
			elif data[0] == "settings":
				self.__cmds.settings.handle_callback(query, data)
		except Exception as e:
			traceback.print_exc()
			for a in self.__cfg.get_log_chats():
				bot.send_message(a, f"An exception occurred to someone ({query.from_user.mention() if query.from_user else 'Unknown'}):\n\n<code>{html.escape(traceback.format_exc())}</code>\nQuery data:\n<code>{html.escape(query.data)}</code>")

	def inlinequery(self, bot, inline):
		LANG = Lang(self.__usr.lang_code(inline.from_user)).string
		if self.__cfg.is_blocked(inline): return # ignore the query
		cache_time = 300
		query = inline.query.split(" ") or ["help"]
		results = []
		if query[0] in ("h", "help"):
			for k, v in LANG('QUERY_COMMANDS').items():
				results += [InlineQueryResultArticle(
					title = v["syntax"],
					input_message_content = InputTextMessageContent(f"""/{v["syntax"]}\n\n{v["description"]}\n\n{LANG('EXAMPLE')}:\n/{v["example"]}"""),
					description = v["description"],
				)]
		elif query[0] in ("e", "encode"):
			results = self.__cmds.convert.inlinequery(LANG, bot, inline)
		elif query[0] in ("info",):
			results = self.__cmds.info.inlinequery(LANG, bot, inline, query)
		elif query[0] in ("p", "pokemon"):
			results = self.__cmds.pokemon.inlinequery(LANG, bot, inline, query)
		elif query[0] in ("pogo",):
			results = self.__cmds.pokemongo.inlinequery(LANG, bot, inline, query)
		elif query[0] in ("tr", "translate"):
			results = self.__cmds.translate.inlinequery(LANG, bot, inline, query)
		elif query[0] in ("wordfor",):
			results = self.__cmds.wordfor.inlinequery(LANG, bot, inline, query)
		elif query[0] in ("scramble", "scr"):
			results = self.__cmds.scramble.inlinequery(LANG, bot, inline, query)
			cache_time = 1
		elif query[0] in ("imdumb", "imsmort", "imdown"):
			text = self.__cmds.misc.retarded(" ".join(query[1:]) or LANG('IM_SMORT'))
			results = [InlineQueryResultArticle(
				title = LANG('CLICK_HERE_TO_BE_RETARDED'),
				input_message_content = InputTextMessageContent(text),
				description = text,
			)]
			cache_time = 1
		else:
			results = [InlineQueryResultArticle(
				title = LANG('QUERY')["help"]["title"],
				input_message_content = InputTextMessageContent(LANG('QUERY')["help"]["content"]),
				description = LANG('QUERY')["help"]["description"],
			)]
		inline.answer(results, cache_time=cache_time)
