from bot.classes import Command
import html
from googletrans import Translator
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

translator = Translator()

class CmdTranslate(Command):
	def function(self, text, d, s) -> str:
		#pass the user and use their default language
		if d in ("auto", "") and s in ("auto", ""):
			translation = translator.translate(text)
		elif d in ("auto", "") and s not in ("auto", ""):
			translation = translator.translate(text, src=s)
		elif d not in ("auto", "") and s in ("auto", ""):
			translation = translator.translate(text, dest=d)
		else:
			translation = translator.translate(text, dest=d, src=s)
		return translation

	def run(self, LANG, bot, message):
		args = (message.text or message.caption).split(" ")
		out = ""
		try:
			d, s = "", ""
			text = " ".join(args[3:])
			if message.reply_to_message is None and (len(args) < 4 or text == ""):
				out = "/translate - Translate a message or some text into another language.\n\nUsage:\n<code>/translate from_language to_language text</code>\n\nExamples:\n<code>/translate auto it Hello Darkness my old friend</code>\n<code>/translate fr en phoque</code>"
			else:
				if text == "":
					text = message.reply_to_message.text or message.reply_to_message.caption
				if len(args) > 2:
					s = args[1]
					d = args[2]
				elif len(args) > 1:
					d = args[1]
				t = self.function(text, d, s)
				if args[0] in ["/translate", "translate"]:
					out = (
						f"""<b>{t.src}</b> → <b>{t.dest}</b>\n\n""" +
						f"""<b>Source:</b>\n{html.escape(t.origin)}\n\n""" +
						f"""<b>Result:</b>\n{html.escape(t.text)}""" #\n\n""" +
						# (f"""<b>Pronunciation:</b> {html.escape(t.pronunciation)}""" if t.pronunciation else "")
					)
				else:
					out = html.escape(t.text)
		except ValueError as e:
			out = "Error: " + str(e)
		
		message.reply_text(out)

	def inline(self, LANG, bot, q):
		if len(q.args) > 3:
			try:
				t = self.function(" ".join(q.args[3:]), q.args[2], q.args[1]).text
				return [InlineQueryResultArticle(
					id = "0",
					title = LANG('TRANSLATION_TITLE'),
					input_message_content = InputTextMessageContent(t),
					description = t,
				)]
			except ValueError as e:
				e = str(e)
				return [InlineQueryResultArticle(
					id = "0",
					title = LANG('ERROR'),
					input_message_content = InputTextMessageContent(e),
					description = e,
				)]
		else:
			return [InlineQueryResultArticle(
				id = "0",
				title = LANG('INVALID_SYNTAX'),
				input_message_content = InputTextMessageContent(LANG('INVALID_SYNTAX') + "\n" + LANG('USAGE') + ": " + LANG('QUERY_COMMANDS')["translate"]["syntax"]),
				description = LANG('USAGE') + ": " + LANG('QUERY_COMMANDS')["translate"]["syntax"],
			)]