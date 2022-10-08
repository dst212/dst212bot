from bot.classes import CallbackQuery, InlineQuery
import logging
log = logging.getLogger(__name__)

from langs import Lang
import traceback, html, base64, json
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class Handlers:
	def __init__(self, users, config, commands):
		self.cfg = config
		self.usr = users
		self.cmds = commands
		self.cmds.map["repeat"] = self
		self.name = "repeat"
		self.args = []
		self.aliases = []
		self.examples = []
		self.inline_args = []

	def run(self, LANG, bot, m): # repeat command
		if m.reply_to_message:
			# do not parse messages from anonymous users or bots (and say just "No.")
			if not m.reply_to_message.from_user or m.reply_to_message.from_user.is_bot:
				m.reply_text(LANG('NO') + ".")
			elif self.cfg.is_admin(m) or (m.from_user and m.from_user.id == m.reply_to_message.from_user.id):
				self.message(bot, m.reply_to_message)
			else:
				m.reply_text(LANG('NO_PERMISSIONS'))
		else:
			m.reply_text(LANG('REPEAT_WHAT'))

	def parse_message(self, bot, m):
		if self.usr.get(m.chat.id, "auto-tr"):
			self.cmds.map["translate"].translate_message(m)
		self.cmds.map["counter"].parse_message(m)
			
	def message(self, bot, m):
		if self.cfg.is_blocked(m):
			#ignore the message but parse it
			self.parse_message(bot, m)
			return
		text = m.text or m.caption
		if text:
			# make emojis valid
			text = text.encode("utf-8").decode("utf-8")
		# allow commands only from non-anonymous and non-bot users, if the message is not send from helpers in a support chat
		if not self.cmds.map["hey"].parse(bot, m) and m.from_user and not m.from_user.is_bot and text and text[0] == "/":
			LANG = Lang(self.usr.lang_code(m), self.cfg).string
			try:
				# run command
				i = text.find(" ")
				cmd = text[1:] if i == -1 else text[1:i]
				i = cmd.find("-")
				if i != -1: cmd = cmd[:i]
				i = cmd.find("@")
				if i != -1: cmd = cmd[:i] if self.cfg.me.username == cmd[i+1:] else ""
				if self.cmds.map.get(cmd): self.cmds.map[cmd].run(LANG, bot, m)
			except Exception as e:
				traceback.print_exc()
				sender = (f"{m.from_user.mention()}, <code>{m.from_user.id}</code>" + (f" at <code>{m.chat.id}</code>" if m.chat.id != m.from_user.id else "")) if m.from_user else "Unknown"
				self.cfg.log(f"<code>#{m.chat.id}</code><code>#{m.id}#</code>\nAn exception occurred to someone ({sender}):\n\n<code>{html.escape(traceback.format_exc())}</code>\nMessage:", forward=[m])
				m.reply_text(LANG('AN_ERROR_OCCURRED_WHILE_PERFORMING'))
		else:
			self.parse_message(bot, m)

	def callback(self, bot, callback):
		if self.cfg.is_blocked(callback): return # ignore the query
		if callback.data:
			try:
				LANG = Lang(self.usr.lang_code(callback), self.cfg).string
				query = CallbackQuery(callback)
				cmd = query.args[0]
				if self.cmds.map.get(cmd):
					self.cmds.map[cmd].callback(LANG, bot, query)
			except Exception as e:
				traceback.print_exc()
				self.cfg.log(f"An exception occurred to someone ({callback.from_user.mention() if callback.from_user else 'Unknown'}):\n\n<code>{html.escape(traceback.format_exc())}</code>\nQuery data:\n<code>{html.escape(callback.data)}</code>")
				callback.answer(LANG('AN_ERROR_OCCURRED_WHILE_PERFORMING'), show_alert = True)
		elif callback.game_short_name:
			payload = base64.b64encode(bytes(json.dumps({"u": callback.from_user.id, "i": callback.inline_message_id}), "utf-8")).decode()
			callback.answer(url=f"https://dst.altervista.org/dst212bot/games/{callback.game_short_name}?{payload}")

	def inline(self, bot, inline):
		if self.cfg.is_blocked(inline): return # ignore the query
		LANG = Lang(self.usr.lang_code(inline), self.cfg).string
		cache_time = 300
		query = InlineQuery(inline)
		cmd = query.args[0] if query.args else "h"
		results = []
		if cmd in ("h", "help"):
			for command, description in LANG('QUERY_COMMANDS').items():
				cmd = self.cmds.map[command]
				example = f"""\n\n{LANG('EXAMPLE')}:\n{cmd.name} {cmd.examples[0]}""" if len(cmd.examples) > 0 else ""
				syntax = f"""{cmd.name} {" ".join(cmd.inline_args)}"""
				results += [InlineQueryResultArticle(
					title = syntax,
					input_message_content = InputTextMessageContent(f"""{syntax}\n\n{description}{example}"""),
					description = description,
				)]
		elif self.cmds.map.get(cmd):
			results = self.cmds.map[cmd].inline(LANG, bot, query)
			cache_time = self.cmds.map[cmd].cache_time
		if not results:
			results = [InlineQueryResultArticle(
				title = LANG('QUERY')["help"]["title"],
				input_message_content = InputTextMessageContent(LANG('QUERY')["help"]["content"]),
				description = LANG('QUERY')["help"]["description"],
			)]
		inline.answer(results, cache_time=cache_time)
