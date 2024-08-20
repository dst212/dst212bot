from bot.classes import BaseCommand
from misc.fun import quick_answer

import base64
import binascii
import html
import traceback

from pyrogram.enums import ParseMode
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent


class CmdEncode(BaseCommand):
    name = "encode"
    args = ["x", "y", "[text]"]
    inline_args = ["x", "y", "text"]
    aliases = ["decode"]
    examples = ["text binary henlo uorld", "b64 t Q2lhbw=="]
    encodings = {
        "binary": ("b", "bin", "binary"),
        "base64": ("b64", "base64"),
        "text": ("t", "txt", "text"),
    }

    def text2base64(self, s: str) -> str:
        return base64.b64encode(bytes(s, "utf-8")).decode()

    def base642text(self, s: str) -> str:
        return str(base64.b64decode(bytes(s, "utf-8")), "utf-8")

    def binary2text(self, s: list) -> str:  # Binary list to text, input must be a list
        return "".join(chr(int(c, 2)) for c in s)

    def text2binary(self, s: str) -> list:
        return [format(ord(c), "08b") for c in s]

    def retrieve_encoding(self, dec: str, enc: str) -> (str, str):
        real_dec, real_enc = None, None
        for k, v in self.encodings.items():
            if not real_dec and dec in v:
                real_dec = k
            if not real_enc and enc in v:
                real_enc = k
            if real_enc and real_dec:
                break
        return real_dec, real_enc

    def function(self, lang, args: list[str]) -> (str, str):
        ok = False
        if len(args) < 4 or not args[3]:
            out = f"{lang.PROVIDE_DECODING_ENCODING_TEXT}\n{lang.EXAMPLE}:\n<code>/encode text binary henlo uorld</code>"
        else:
            out = args[3]
            dec, enc = self.retrieve_encoding(args[1].lower(), args[2].lower())
            if dec and enc:
                if dec == enc:
                    out = lang.YOU_SHOULD_KNOW
                else:
                    try:
                        # decode from
                        if dec == "binary":
                            out = self.binary2text(out.split(" "))
                        elif dec == "base64":
                            out = self.base642text(out)
                        # encode to
                        if enc == "binary":
                            out = " ".join(self.text2binary(out))
                        elif enc == "base64":
                            out = self.text2base64(out)
                        ok = True
                    except binascii.Error:
                        out = lang.ENCODE_PROVIDED_ISNT.format("base64")
                    except (UnicodeError, Exception):
                        out = lang.ENCODE_ERROR
                        traceback.print_exc()
                    except ValueError:
                        out = lang.ENCODE_PROVIDED_ISNT.format("binary")
                        traceback.print_exc()
            elif not dec and enc:
                out = lang.ENCODE_IS_NOT_VALID.format(html.escape(args[1]))
            elif not enc and dec:
                out = lang.ENCODE_IS_NOT_VALID.format(html.escape(args[2]))
            else:
                out = lang.ENCODE_ARE_NOT_VALID.format(
                    html.escape(args[1]), html.escape(args[2])
                )
        return out, ok

    async def run(self, bot, m):
        args = (m.text or m.caption).split(" ", 3)
        if len(args) < 4 and m.reply_to_message:
            args.append(m.reply_to_message.text or m.reply_to_message.caption)
        text, ok = self.function(m.lang, args)
        await m.reply(f"<code>{html.escape(text)}</code>" if ok else html.escape(text))

    async def inline(self, bot, q):
        args = q.query.split(" ", 3)
        if len(args) < 4:
            await quick_answer(q, q.lang.PROVIDE_DECODING_ENCODING_TEXT, "h_encode")
        else:
            output, _ = self.function(q.lang, args)
            await q.answer([
                InlineQueryResultArticle(
                    title=q.lang.ENCODE_FROM_TO.format("", args[1], args[2]),
                    input_message_content=InputTextMessageContent(
                        f"<code>{html.escape(output)}</code>", parse_mode=ParseMode.HTML),
                    description=output,
                )
            ], cache_time=self.cache_time)
