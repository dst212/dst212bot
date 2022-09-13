from bot.classes import Command
from custom.log import log
from custom.misc import can_delete, sender_is_admin
import html, random

class CmdRaiseError(Command):
	def run(self, LANG, bot, m):
		raise Warning("This is a test.")

class CmdMsgInfo(Command):
	def run(self, LANG, bot, m):
		m.reply_text("<code>" + html.escape(str(m.reply_to_message or m)) + "</code>")

class CmdCount(Command):
	def run(self, LANG, bot, m):
		m.reply_text(str(m.id - m.reply_to_message.id if m.reply_to_message else m.id))

class CmdLength(Command):
	def run(self, LANG, bot, m):
		m.reply_text(len(" ".join((m.text or m.caption).split(" ")[1:]) or ("" if m.reply_to_message is None else (m.reply_to_message.text or m.reply_to_message.caption))))

class CmdPing(Command):
	def run(self, LANG, bot, m):
		m.reply_text("Pong")

class CmdPurge(Command):
	def run(self, LANG, bot, m):
		if not sender_is_admin(m):
			m = m.reply_text(LANG("NO"))
			time.sleep(3)
			if can_delete(m):
				bot.delete_messages(m.chat.id, [m.id, m.id])
			else:
				m.delete()
		elif can_delete(m):
			bot.delete_messages(m.chat.id, range(m.reply_to_message.id if m.reply_to_message else m.id, m.id + 1))

class CmdSay(Command):
	def run(self, LANG, bot, m):
		text = m.text or m.caption
		i = text.find(" ")
		text = "⁭ " if i == -1 else text[i + 1:]
		if text:
			if can_delete(m):
				bot.delete_messages(m.chat.id, m.id)
			if m.reply_to_message:
				m.reply_to_message.reply_text(text, reply_to_message_id=m.reply_to_message.id)
			else:
				bot.send_message(m.chat.id, text)

class CmdTPB(Command):
	def run(self, LANG, bot, m):
		m.reply_text("⛵️🛵🍆\n💪  | 🤳\n        |\n       /\\\n     /    \\")

class CmdImDumb(Command):
	def function(self, t):
		out = ""
		b = True
		for i in t:
			if i.isalpha():
				out += i.upper() if b else i.lower()
				b = not b
			elif i == "!":
				if random.random() < 0.5:
					out += i
				else:
					out += "1"
			else:
				out += i
		return out or "I'm SmOrT!1!1!"

	def run(self, LANG, bot, m):
		m.reply(self.function(m.text or m.caption))

	def inline(self, LANG, bot, q):
		return [InlineQueryResultArticle(
			title = LANG('CLICK_HERE_TO_BE_RETARDED'),
			input_message_content = InputTextMessageContent(text),
			description = " ".join(q.args[1:]) or LANG('IM_SMORT'),
		)]