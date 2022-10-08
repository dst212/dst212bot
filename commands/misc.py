from bot.classes import BaseCommand
from custom.misc import can_delete, sender_is_admin

import html, logging, os, random
log = logging.getLogger(__name__)

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

# /msgi
class CmdMsgInfo(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "msgi"
		self.base_dir = f"./data/cache/{self.name}/"

	def run(self, LANG, bot, m):
		args = (m.text or m.caption).split(" ")
		if m.reply_to_message:
			m = m.reply_to_message
		output = str(m)
		if len(output) < 4096 and len(args) > 1 and args[1] == "here":
			m.reply_text("<code>" + html.escape(output) + "</code>")
		else:
			os.makedirs(self.base_dir, exist_ok=True)
			filepath = f"{self.base_dir}/{m.chat.id}-{m.id}.json"
			if not os.path.exists(filepath):
				with open(filepath, "w") as f:
					f.write(output)
			m.reply_document(filepath)

# /count
class CmdCount(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "count"

	def run(self, LANG, bot, m):
		m.reply_text(str(m.id - m.reply_to_message.id if m.reply_to_message else m.id))

# /len
class CmdLength(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "len"
		self.args = ["[text]"]

	def run(self, LANG, bot, m):
		m.reply_text(str(len(" ".join((m.text or m.caption).split(" ")[1:]) or ("" if m.reply_to_message is None else (m.reply_to_message.text or m.reply_to_message.caption)))))

# /ping
class CmdPing(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "ping"

	def run(self, LANG, bot, m):
		m.reply_text("Pong")

# /delall
class CmdPurge(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "delall"

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

# /say
class CmdSay(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "say"
		self.args = ["text"]

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

# /tpb
class CmdTPB(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "tpb"

	def run(self, LANG, bot, m):
		m.reply_text("⛵️🛵🍆\n💪  | 🤳\n        |\n       /\\\n     /    \\")

# /imdumb
class CmdImDumb(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "imdumb"
		self.args = ["[text]"]
		self.inline_args = ["text"]
		self.examples = ["im super smort"]
		self.cache_time = 1

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
		return out

	def run(self, LANG, bot, m):
		text = (m.text or m.caption)
		i = text.find(" ")
		if i == -1:
			m.reply(LANG('WE_ALL_KNOW_THAT'))
		else:
			text = text[i+1:]
			m.reply(self.function(text))

	def inline(self, LANG, bot, q):
		text = self.function(" ".join(q.args[1:]) or LANG('IM_SMORT'))
		return [InlineQueryResultArticle(
			title = LANG('CLICK_HERE_TO_BE_RETARDED'),
			input_message_content = InputTextMessageContent(text),
			description = text,
		)]
