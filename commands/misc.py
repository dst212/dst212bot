from custom.log import log
from custom.misc import can_delete, sender_is_admin
import html, random

class Misc:
	def __init__(self, users):
		self.__usr = users

	def raise_error(self, bot, message):
		raise Warning("This is a test.")

	def retarded(self, t):
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

	def message_info(self, LANG, bot, message):
		message.reply_text("<code>" + html.escape(str(message.reply_to_message or message)) + "</code>")

	def count_messages(self, LANG, bot, message):
		message.reply_text(str(message.id - message.reply_to_message.id if message.reply_to_message else message.id))

	def message_length(self, LANG, bot, message):
		message.reply_text(len(" ".join((message.text or message.caption).split(" ")[1:]) or ("" if message.reply_to_message is None else (message.reply_to_message.text or message.reply_to_message.caption))))

	def pong(self, LANG, bot, message):
		message.reply_text("Pong")

	def purge(self, LANG, bot, message):
		if not sender_is_admin(message):
			m = message.reply_text(LANG("NO"))
			time.sleep(3)
			if can_delete(message):
				bot.delete_messages(message.chat.id, [m.id, message.id])
			else:
				m.delete()
		elif can_delete(message):
			bot.delete_messages(message.chat.id, range(message.reply_to_message.id if message.reply_to_message else message.id, message.id + 1))

	def say(self, LANG, bot, message):
		text = message.text or message.caption
		i = text.find(" ")
		text = "⁭ " if i == -1 else text[i + 1:]
		if text:
			if can_delete(message):
				bot.delete_messages(message.chat.id, message.id)
			if message.reply_to_message:
				message.reply_to_message.reply_text(text, reply_to_message_id=message.reply_to_message.id)
			else:
				bot.send_message(message.chat.id, text)

	def tpb(self, LANG, bot, message):
		message.reply_text("⛵️🛵🍆\n💪  | 🤳\n        |\n       /\\\n     /    \\")
