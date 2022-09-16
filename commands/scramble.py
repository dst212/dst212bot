from bot.classes import Command
import random
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class CmdScramble(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cache_time = 1

	def function(self, s: str) -> str:
		t = list(s)
		s = []
		for _ in range(len(t)):
			s += [t.pop(int(random.random()*len(t)))]
		return "".join(s)

	def run(self, LANG, bot, m):
		text = None
		if m.reply_to_message is None:
			text = (m.text or m.caption)
			text = text[text.find(" ") + 1 or len(text):]
		else:
			text = (m.reply_to_message.text or m.reply_to_message.caption)
		if text:
			m.reply_text(self.function(text))
		else:
			m.reply_text(LANG('PROVIDE_TEXT'))

	def inline(self, LANG, bot, q):
		text = self.function(q.text[len(q.args[0])+1:])
		return [InlineQueryResultArticle(
			id = "0",
			title = LANG('SCRAMBLE_TEXT'),
			input_message_content = InputTextMessageContent(text),
			description = text,
		)]