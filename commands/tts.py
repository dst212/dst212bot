from bot.classes import BaseCommand

import asyncio
import gtts
import html
import logging
import os
import traceback

from googletrans import Translator
from hashlib import md5

log = logging.getLogger(__name__)


class CmdTTS(BaseCommand):
    name = "tts"
    args = ["[text]"]
    base_dir = "data/cache/audio/"
    translator = Translator()

    async def run(self, bot, m):
        os.makedirs(self.base_dir, exist_ok=True)
        text = ((m.text or m.caption).split(" ", 1)[1:] or [""])[0]
        lang = None
        if text.startswith("#"):
            # Get the lang from the text
            # (example: "#it Oh sole mio" makes the text "Oh sole mio" Italian)
            lang, text, *_ = text[1:].split(" ", 1) + [None]
        # Get text to turn into speech
        if not text:
            if m.reply_to_message:
                text = m.reply_to_message.text or m.reply_to_message.caption
        if not text:
            await m.reply_text(m.lang.PROVIDE_TEXT)
            return
        # Start doing stuff
        r = await m.reply(m.lang.PROCESSING)
        tts_langs = gtts.lang.tts_langs()
        if not lang:
            lang = self.translator.detect(text.split("\n", 1)[0]).lang
            if isinstance(lang, list):
                for i in lang:
                    if i in tts_langs:
                        lang = i
                        break
            if lang not in tts_langs:
                lang = "en"
        elif lang not in tts_langs:
            await r.edit(
                m.lang.LANGUAGE_IS_NOT_SUPPORTED.format(html.escape(lang))
                + "\n"
                + m.lang.USING_LANGUAGE.format("en")
            )
            lang = "en"
        filepath = f"{self.base_dir}{md5(text.encode()).hexdigest()}.{lang}.mp3"
        # Save the speech to a file
        if not os.path.exists(filepath):
            await r.edit(m.lang.CREATING)
            try:
                fun = await asyncio.to_thread(gtts.gTTS, text, lang=lang)
                await asyncio.to_thread(fun.save, filepath)
            except Exception:
                traceback.print_exc()
                log.error(f"{lang} {text}")
                await r.edit(m.lang.ERROR_WHILE_CREATING_FILE)
                return
        await r.edit(m.lang.UPLOADING)
        with open(filepath, "rb") as f:
            await bot.send_audio(
                r.chat.id,
                f,
                reply_to_message_id=m.id,
                file_name=f"text-to-speech.{lang}.mp3",
                caption="Audio for text:\n"
                f"<code>{html.escape(text[:1000])}</code>",
            )
        await r.delete()

    # TODO inlinequery
