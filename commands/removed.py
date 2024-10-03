from bot.classes import BaseCommand

from pyrogram.enums import ParseMode


class CmdPoGo(BaseCommand):
    name = "pogo"

    async def run(self, bot, m):
        await m.reply(
            "`/pogo` was removed.\n"
            "Use [@pogomatchbot](https://pogomatchbot.t.me)!\n"
            "The equivalent command is `/rank`.",
            parse_mode=ParseMode.MARKDOWN,
        )


class CmdInfo(BaseCommand):
    name = "info"

    async def run(self, bot, m):
        await m.reply(
            "`/info` was moved to [@shadowseyebot](https://shadowseyebot.t.me)!",
            parse_mode=ParseMode.MARKDOWN,
        )


class CmdHey(BaseCommand):
    name = "hey"
    aliases = ["bye"]

    async def run(self, bot, m):
        await m.reply(
            "`/hey` was replaced with /feedback.",
            parse_mode=ParseMode.MARKDOWN,
        )


class CmdMsgi(BaseCommand):
    name = "msgi"

    async def run(self, bot, m):
        await m.reply(
            "`/msgi` was replaced with /inspect.",
            parse_mode=ParseMode.MARKDOWN,
        )


class CmdCount(BaseCommand):
    name = "count"

    async def run(self, bot, m):
        await m.reply(
            "`/count` was removed.",
            parse_mode=ParseMode.MARKDOWN,
        )


class CmdDelAll(BaseCommand):
    name = "delall"

    async def run(self, bot, m):
        await m.reply(
            "`/delall` was removed.",
            parse_mode=ParseMode.MARKDOWN,
        )
