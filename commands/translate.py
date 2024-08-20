from bot.classes import BaseCommand
from misc.fun import quick_answer
from custom import command_entry

import googletrans
import html
import logging
import re
import translators as ts

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

log = logging.getLogger(__name__)


class CmdTranslate(BaseCommand):
    _max_length = 3900  # Maximum length for translated messages output
    _legacy = True
    name = "translate"
    args = ["from_lang", "to_lang", "[text]"]
    inline_args = ["from_lang", "to_lang", "text"]
    aliases = ["tr"]
    examples = ["auto it hello darkness my old friend", "en ja hello"]
    translator = googletrans.Translator()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # what should not be translated
        self.exclusions = (
            "ok",
            "lol",
            "lmao",
            "lmfao",
            "kek",
            "kekw",
        )  # TODO: add a file for this
        if (self._legacy):
            log.info("Using legacy translate-mode (googletrans).")

    async def translate_message(self, m):
        text = m.text or m.caption
        if (
            not text
            or (not await self.usr.get(m.chat, "tr-commands") and re.match(r"^/[A-Za-z0-9]", text))
            or text.lower() in self.exclusions
        ):
            return
        text = text.replace("\n", "  ")
        dest = await self.usr.get(m.chat, "auto-tr")
        if not isinstance(dest, str) or dest == "off":
            return
        if dest == "auto":
            dest = await self.usr.lang_code(m.chat.id)
        src = self.translator.detect(text).lang
        if isinstance(src, list) and dest not in src:
            detected = src
            src = detected.pop(0)
            while src and src not in googletrans.LANGUAGES:
                log.warning(f"Leaving {src}, unknown langauge.")
                src = detected.pop(0) if len(detected) > 0 else None
        elif isinstance(src, str) and src not in googletrans.LANGUAGES:
            log.warning(f"Leaving '{src}', unknown langauge.")
            log.warning(
                "Using auto detect of translate() which works if no src is provided."
            )
            src = None
        if not isinstance(src, list) and dest != src:
            out = await self.function(m, text, dest, src or "auto")
            if out.text.lower() == text.lower():
                return
            i = out.text.rfind(" ") if len(out.text) > self._max_length else -1
            if i == -1 or i > self._max_length:
                i = self._max_length
            first = await m.reply(
                f"[<code>AUTO-TR {googletrans.LANGUAGES.get(src) or "unknown"} ({out.src})</code>]\n"
                f"{html.escape(out.text[:i])}"
            )
            if len(out.text) > i:
                await first.reply(html.escape(out.text[i:]))

    async def function(self, m, text, d, s):
        if d in ("auto", ""):
            d = await self.usr.lang_code(m)
        if self._legacy:
            return self.translator.translate(text, dest=d, src=s or "auto")
        return ts.translate_text(text, translator="google", from_language=s, to_language=d)

    async def run(self, bot, m):
        args = (m.text or m.caption).split(" ")
        out = ""
        try:
            d, s = "", ""
            text = " ".join(args[3:])
            if m.reply_to_message is None and (len(args) < 4 or text == ""):
                out = command_entry(m.lang, self)
            else:
                if text == "":
                    text = m.reply_to_message.text or m.reply_to_message.caption
                if len(args) > 2:
                    s = args[1]
                    d = args[2]
                elif len(args) > 1:
                    d = args[1]
                t = await self.function(m, text, d, s)
                if self._legacy and args[0] in ["/" + self.name, self.name]:
                    out = (
                        f"<b>{t.src}</b> → <b>{t.dest}</b>\n\n"
                        f"<b>{m.lang.SOURCE_TEXT}:</b>\n{html.escape(t.origin)}\n\n"
                        f"<b>{m.lang.RESULT}:</b>\n{html.escape(t.text)}"
                    )
                else:
                    out = html.escape(t.text if self._legacy else t)
        except ValueError as e:
            out = f"{m.lang.ERROR}: {e}"

        await m.reply_text(out)

    async def inline(self, bot, q):
        args = q.query.split(" ", 3)
        if len(args) > 3:
            t = await self.function(
                q, args[3], args[2], args[1])
            if self._legacy:
                t = t.text
            await q.answer([
                InlineQueryResultArticle(
                    title=q.lang.TRANSLATION_TITLE,
                    input_message_content=InputTextMessageContent(t),
                    description=t,
                )
            ], cache_time=self.cache_time)
        else:
            await quick_answer(q, f"{self.name} <src> <dest> <text>", "h_translate")
