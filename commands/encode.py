from bot.classes import Command
from langs import en as LANG
import base64, html, traceback, binascii
from pyrogram.enums import ParseMode

class CmdEncode(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "encode"
		self.args = ["x", "y", "[text]"]
		self.inline_args = ["x", "y", "text"]
		self.aliases = ["e"]
		self.examples = ["text binary henlo uorld", "b64 t Q2lhbw=="]
		self.encodings = {
			"binary": ("b", "bin", "binary"),
			"base64": ("b64", "base64"),
			"text": ("t", "txt", "text")
		}
	def text2base64(self, s: str) -> str:
		return base64.b64encode(bytes(s, "utf-8")).decode()
	def base642text(self, s: str) -> str:
		return str(base64.b64decode(bytes(s, "utf-8")), "utf-8")
	def binary2text(self, s: list) -> str: #binary list to text, input must be a list
		return "".join(chr(int(c,2)) for c in s)
	def text2binary(self, s: str) -> list:
		return [format(ord(c),"08b") for c in s]

	def retrieve_encoding(self, dec: str, enc: str) -> (str, str):
		real_dec, real_enc = None, None
		for k, v in self.encodings.items():
			if not real_dec and dec in v: real_dec = k
			if not real_enc and enc in v: real_enc = k
			if real_enc and real_dec: break
		return real_dec, real_enc

	def function(self, LANG, args, alternate_text: str) -> (str, str):
		out, ok = "", False
		if (len(args) < 4 and alternate_text == "") or (len(args) < 3 and alternate_text != ""):
			out = f"{LANG('PROVIDE_DECODING_ENCODING_TEXT')}\n{LANG('EXAMPLE')}:\n<code>/encode text binary henlo uorld</code>"
		else:
			out = args[3:] or alternate_text
			dec, enc = self.retrieve_encoding(args[1].lower(), args[2].lower())
			if dec and enc:
				if dec == enc: out = LANG('YOU_SHOULD_KNOW')
				else:
					try:
						#decode from
						if dec == "binary":		out = self.binary2text(out)
						elif dec == "base64":	out = self.base642text(" ".join(out))
						elif dec == "text":		out = " ".join(out)
						#encode to
						if enc == "binary":		out = " ".join(self.text2binary(out))
						elif enc == "base64":	out = self.text2base64(out)
						ok = True
					except binascii.Error as e:
						out = LANG('ENCODE_PROVIDED_ISNT').format("base64")
					except ValueError as e:
						out = LANG('ENCODE_PROVIDED_ISNT').format("binary")
					except Exception as e:
						out = LANG('ENCODE_ERROR')
						print(traceback.format_exc())
			elif not dec and enc:
				out = LANG('ENCODE_IS_NOT_VALID').format(html.escape(args[1]))
			elif not enc and dec:
				out = LANG('ENCODE_IS_NOT_VALID').format(html.escape(args[2]))
			else:
				out = LANG('ENCODE_ARE_NOT_VALID').format(html.escape(args[1]), html.escape(args[2]))
		return out, ok

	def run(self, LANG, bot, m):
		text, ok = self.function(LANG, (m.text or m.caption).split(" "), "" if m.reply_to_message is None else (m.reply_to_message.text or m.reply_to_message.caption).split(" "))
		m.reply_text("<code>" + html.escape(text) + "</code>" if ok else text)

	def inline(self, LANG, bot, q):
		if len(q.args) < 4:
			return [InlineQueryResultArticle(
				id = "0",
				title = LANG('INVALID_SYNTAX'),
				input_message_content = InputTextMessageContent(LANG('PROVIDE_DECODING_ENCODING_TEXT')),
				description = LANG('PROVIDE_DECODING_ENCODING_TEXT'),
			)]
		else:
			output, _ = self.function(LANG, q.args, "")
			return [InlineQueryResultArticle(
				id = "0",
				title = LANG('ENCODE_FROM_TO').format("", q.args[1], q.args[2]),
				input_message_content = InputTextMessageContent(f"<code>{html.escape(output)}</code>", parse_mode=ParseMode.HTML),
				description = output,
			)]
