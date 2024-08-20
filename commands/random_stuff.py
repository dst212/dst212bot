from bot.classes import BaseCommand

import html
import random

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent


# /random
class CmdRand(BaseCommand):
    name = "random"
    args = ["[x]", "[y]"]
    aliases = ["rand"]

    def function(self, args: list) -> int:
        min_num = 0
        max_num = 100
        try:
            min_num = int(args[1])
        except Exception:
            pass
        try:
            max_num = int(args[2])
        except Exception:
            max_num += min_num
        if min_num > max_num:
            min_num, max_num = max_num, min_num
        elif min_num == max_num:
            max_num += 1
        return random.randrange(min_num, max_num)

    async def run(self, bot, m):
        await m.reply(self.function((m.text or m.caption).split(" ")))


# /pickrandom
class CmdPickRandom(BaseCommand):
    name = "pickrandom"
    args = ["[limit]"]
    aliases = ["pr"]

    def function(self, items: list, limit=1):
        out = ""
        if limit > len(items):
            limit = len(items)
        for i in range(limit):
            out += items.pop(random.randrange(0, len(items))) + "\n"
        return out

    async def run(self, bot, m):
        if not m.reply_to_message:
            await m.reply(m.lang.PICK_RANDOM_REPLY_TO_A_MESSAGE)
        else:
            args = (m.text or m.caption).split(" ")
            out = ""
            limit = 1
            if len(args) > 1:
                try:
                    limit = int(args[1])
                    if limit < 1:
                        raise ValueError
                except ValueError:
                    out = m.lang.IS_INVALID_USING.format(html.escape(args[1]), 1)
            out += self.function(
                (m.reply_to_message.text or m.reply_to_message.caption).split("\n"),
                limit,
            )
            await m.reply(html.escape(out))


# /shuffle
class CmdShuffle(BaseCommand):
    name = "shuffle"
    args = ["[text]"]
    inline_args = ["text"]
    cache_time = 1

    def function(self, s: str) -> str:
        t = list(s)
        s = []
        for _ in range(len(t)):
            s += [t.pop(int(random.random() * len(t)))]
        return "".join(s)

    async def run(self, bot, m):
        text = None
        if m.reply_to_message is None:
            text = m.text or m.caption
            text = text[text.find(" ")+1 or len(text):]
        else:
            text = m.reply_to_message.text or m.reply_to_message.caption
        if text:
            await m.reply(self.function(text))
        else:
            await m.reply(m.lang.PROVIDE_TEXT)

    async def inline(self, bot, q):
        text = self.function((q.query.strip().split(" ", 1)[1:] or [q.lang.WRITE_SOME_TEXT])[0])
        await q.answer([
            InlineQueryResultArticle(
                title=q.lang.SHUFFLE_TEXT,
                input_message_content=InputTextMessageContent(text),
                description=text,
            )
        ], cache_time=self.cache_time)
