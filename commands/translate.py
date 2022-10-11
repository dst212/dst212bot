from bot.classes import BaseCommand
from custom.misc import command_entry

import googletrans, html, logging
log = logging.getLogger(__name__)

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class CmdTranslate(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "translate"
		self.args = ["from_lang", "to_lang", "[text]"]
		self.inline_args = ["from_lang", "to_lang", "text"]
		self.aliases = ["tr"]
		self.examples = ["auto it hello darkness my old friend", "en ja hello"]

		self.translator = googletrans.Translator()
		# what should not be translated
		self.exclusions = ("ok", "lol", "lmao", "lmfao", "kek", "kekw", ) # TODO: add a file for this
		self._max_length = 3900 #maximum length for translated messages output

	def translate_message(self, m):
		text = m.text or m.caption
		if not text or text.lower() in self.exclusions:
			return
		dest = self.usr.get(m.chat.id, "auto-tr")
		if dest == "auto":
			dest = self.usr.lang_code(m.chat.id)
		src = self.translator.detect(text).lang
		if type(src) == list and dest not in src:
			detected = src
			src = detected.pop(0)
			while src and src not in googletrans.LANGUAGES:
				log.warning(f"Leaving {src}, unknown langauge.")
				src = detected.pop(0) if len(detected) > 0 else None
		elif type(src) == str and src not in googletrans.LANGUAGES:
			log.warning(f"Leaving '{src}', unknown langauge.")
			log.warning("Using auto detect of translate() which works if no src is provided.")
			src = None
		if type(src) != list and dest != src:
			out = self.translator.translate(text, src=src or "auto", dest=dest)
			if out.text == text:
				return
			first = m.reply_text(f"""[<code>AUTO-TR {googletrans.LANGUAGES.get(src) or "unknown"} ({out.src})</code>]\n""" + html.escape(out.text[:self._max_length]))
			if len(out.text) > self._max_length:
				first.reply_text(html.escape(out.text[self._max_length:]))

	def function(self, m, text, d, s):
		if d in ("auto", ""):
			d = self.usr.lang_code(m)
		return self.translator.translate(text, dest=d, src=s or "auto")

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
				t = self.function(m, text, d, s)
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
				t = self.function(q.inline, " ".join(q.args[3:]), q.args[2], q.args[1]).text
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
