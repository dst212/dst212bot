import random
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class Scramble:
	def __init__(self, users):
		self.__usr = users

	def function(self, s: str) -> str:
		t = list(s)
		s = []
		for _ in range(len(t)):
			s += [t.pop(int(random.random()*len(t)))]
		return "".join(s)

	def command(self, LANG, bot, message):
		text = None
		if message.reply_to_message is None:
			text = (message.text or message.caption)
			text = text[text.find(" ") + 1 or len(text):]
		else:
			text = (message.reply_to_message.text or message.reply_to_message.caption)
		if text:
			message.reply_text(self.function(text))
		else:
			message.reply_text(LANG('PROVIDE_TEXT'))

	def inlinequery(self, LANG, bot, inline, query):
		text = self.function(inline.query[inline.query.find(" ")+1:])
		return [InlineQueryResultArticle(
			id = "0",
			title = LANG('SCRAMBLE_TEXT'),
			input_message_content = InputTextMessageContent(text),
			description = text,
		)]