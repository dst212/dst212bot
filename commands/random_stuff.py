from bot.classes import BaseCommand

import random

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent


# /random
class CmdRand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "random"
        self.args = ["[x]", "[y]"]
        self.aliases = ["r"]

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

    def run(self, LANG, bot, m):
        m.reply_text(self.function((m.text or m.caption).split(" ")))


# /pickrandom
class CmdPickRandom(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "pickrandom"
        self.args = ["[limit]"]
        self.aliases = ["pr"]

    def function(self, items: list, limit=1):
        out = ""
        if limit > len(items):
            limit = len(items)
        for i in range(limit):
            out += items.pop(random.randrange(0, len(items))) + "\n"
        return out

    def run(self, LANG, bot, m):
        if not m.reply_to_message:
            m.reply_text(LANG("PICK_RANDOM_REPLY_TO_A_MESSAGE"))
        else:
            args = (m.text or m.caption).split(" ")
            out = ""
            limit = 1
            if len(args) > 1:
                try:
                    limit = int(args[1])
                    if limit < 1:
                        raise ValueError("Limit must be greater than 1")
                except Exception:
                    out = LANG("IS_INVALID_USING").format(args[1], 1)
            out += self.function(
                (m.reply_to_message.text or m.reply_to_message.caption).split("\n"),
                limit,
            )
            m.reply_text(out)


# /shuffle
class CmdShuffle(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "shuffle"
        self.args = ["[text]"]
        self.inline_args = ["text"]
        self.cache_time = 1

    def function(self, s: str) -> str:
        t = list(s)
        s = []
        for _ in range(len(t)):
            s += [t.pop(int(random.random() * len(t)))]
        return "".join(s)

    def run(self, LANG, bot, m):
        text = None
        if m.reply_to_message is None:
            text = m.text or m.caption
            text = text[text.find(" ")+1 or len(text):]
        else:
            text = m.reply_to_message.text or m.reply_to_message.caption
        if text:
            m.reply_text(self.function(text))
        else:
            m.reply_text(LANG("PROVIDE_TEXT"))

    def inline(self, LANG, bot, q):
        text = self.function(q.text[len(q.args[0])+1:])
        return [
            InlineQueryResultArticle(
                id="0",
                title=LANG("SHUFFLE_TEXT"),
                input_message_content=InputTextMessageContent(text),
                description=text,
            )
        ]
