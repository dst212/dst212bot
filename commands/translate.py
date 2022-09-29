from bot.classes import Command
from custom.misc import command_entry
import googletrans, html
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class CmdTranslate(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "translate"
		self.args = ["from_lang", "to_lang", "[text]"]
		self.inline_args = ["from_lang", "to_lang", "text"]
		self.aliases = ["tr"]
		self.examples = ["auto it hello darkness my old friend", "en ja hello"]

		self.translator = googletrans.Translator()

	def translate_message(self, m):
		text = m.text or m.caption
		dest = self.usr.lang_code(m.chat.id)
		src = self.translator.detect(text).lang
		if type(src) == list and dest not in src:
			src = src[0]
		if type(src) != list and dest != src:
			m.reply_text("[<code>AUTO-TR</code>] " + html.escape(self.translator.translate(text, src=src, dest=dest).text))

	def function(self, text, d, s):
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

	def run(self, LANG, bot, m):
		args = (m.text or m.caption).split(" ")
		out = ""
		try:
			d, s = "", ""
			text = " ".join(args[3:])
			if m.reply_to_message is None and (len(args) < 4 or text == ""):
				out = command_entry(LANG, self)
			else:
				if text == "":
					text = m.reply_to_message.text or m.reply_to_message.caption
				if len(args) > 2:
					s = args[1]
					d = args[2]
				elif len(args) > 1:
					d = args[1]
				t = self.function(text, d, s)
				if args[0] in ["/"+self.name, self.name]:
					out = (
						f"<b>{t.src}</b> → <b>{t.dest}</b>\n\n" +
						f"<b>{LANG('SOURCE_TEXT')}:</b>\n{html.escape(t.origin)}\n\n" +
						f"<b>{LANG('RESULT')}:</b>\n{html.escape(t.text)}"
					)
				else:
					out = html.escape(t.text)
		except ValueError as e:
			out = f"{LANG('ERROR')}: {e}"
		
		m.reply_text(out)

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