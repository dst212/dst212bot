#!/usr/bin/env python3
from keys import TOKEN, API_ID, API_HASH
from config import BOTNAME, ADMINS, LOG_CHAT, SUPPORT_CHAT
from misc import commands
from misc.sudo import SudoConfig

from bot.users import Users
from commands import Commands

import asyncio
import logging
import socket
import sys
import uvloop

from pyrogram import Client, idle
from pyrogram.enums import ParseMode

logging.basicConfig(
    format="[%(asctime)s|%(levelname)s] - %(name)s - %(message)s", level=logging.INFO)
log = logging.getLogger(BOTNAME)


def ping_server() -> bool:
    try:
        with socket.socket() as s:
            s.connect(("api.telegram.org", 443))
    except socket.error:
        return False
    return True


async def main():
    if not ping_server():
        log.info("Waiting for connection...")
        while not ping_server():
            await asyncio.sleep(20)

    bot = Client(BOTNAME, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
    bot.set_parse_mode(ParseMode.HTML)

    usr = Users(bot)

    async def list_chats(bot, m):
        r = await m.reply(m.lang.LOADING)
        chats = await usr.get_active_chats()
        await r.edit(
            f"{"\n".join(f"{k}: {len(v)}" for k, v in chats.items() if isinstance(v, dict))}\n\n"
            f"{m.lang.TOTAL}: {chats["count"]}")

    sudo = SudoConfig(
        bot,
        admins=ADMINS,
        log_chat=LOG_CHAT,
        prefix="%",
        get_chats=usr.get_active_chats_list,
        error_message=(
            "An error occurred.\n"
            "Please, contact @dst212 for further information."
        ),  # TODO: support for intl here
        block_system=True,
        commands={
            "users": list_chats,
        }
    )
    commands.init("id", bot)
    commands.init("ping", bot)
    commands.init("inspect", bot)
    commands.init("feedback", bot, sudo, SUPPORT_CHAT)

    Commands(bot, usr, sudo)

    # users = Users(bot)
    # config = Config(bot, users)
    # await config.init()
    # handlers = Handlers(users, config, Commands(bot, users, config))

    log.info("Starting bot...")
    async with bot:
        log.info("Bot started.")
        await sudo.log("Bot started.")

        log.info("Idling...")
        await idle()

        await sudo.log("Bot stopped.")
        log.info("Stopping...")
    log.info("Bot stopped.")

    sys.exit(0)


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
