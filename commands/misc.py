from bot.classes import BaseCommand
from misc.fun import can_delete

import html
import logging
import random

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

log = logging.getLogger(__name__)


# /len
class CmdLength(BaseCommand):
    name = "len"
    args = ["[text]"]

    async def run(self, bot, m):
        await m.reply(str(len(
            ((m.text or m.caption).split(" ", 1)[1:] or [""])[0]
            or (
                "" if m.reply_to_message is None
                else (m.reply_to_message.text or m.reply_to_message.caption)
            )
        )))


# /say
class CmdSay(BaseCommand):
    name = "say"
    args = ["text"]

    async def run(self, bot, m):
        text = (m.text or m.caption).split(" ", 1)[1:]
        text = text[0] if text else "⁭"
        if text:
            if await can_delete(m):
                await bot.delete_messages(m.chat.id, m.id)
            await bot.send_message(m.chat.id, text, reply_to_message_id=m.reply_to_message_id)


# /tpb
class CmdTPB(BaseCommand):
    name = "tpb"

    async def run(self, bot, m):
        await m.reply("⛵️🛵🍆\n💪  | 🤳\n        |\n       /\\\n     /    \\")


# /imdumb
class CmdImDumb(BaseCommand):
    name = "imdumb"
    args = ["[text]"]
    inline_args = ["text"]
    examples = ["im super smort"]
    cache_time = 1

    def function(self, t):
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
        return out

    async def run(self, bot, m):
        text = m.text or m.caption
        i = text.find(" ")
        if i == -1:
            await m.reply(m.lang.WE_ALL_KNOW_THA)
        else:
            text = text[i+1:]
            await m.reply(self.function(text))

    async def inline(self, bot, q):
        text = self.function((q.query.strip().split(" ", 1)[1:] or [q.lang.IM_SMORT])[0])
        await q.answer([
            InlineQueryResultArticle(
                title=q.lang.CLICK_HERE_TO_BE_RETARDED,
                input_message_content=InputTextMessageContent(html.escape(text)),
                description=text,
            )
        ], cache_time=self.cache_time)
