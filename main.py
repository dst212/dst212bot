#!/usr/bin/env python3
from variables import TOKEN, API_ID, API_HASH, BOTNAME
from bot.config import Config
from bot.handlers import Handlers
from bot.users import Users
from commands import Commands

import logging
import socket
import sys
import time

from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler, InlineQueryHandler, CallbackQueryHandler
from pyrogram.enums import ParseMode

logging.basicConfig(
    format="[%(asctime)s] - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(BOTNAME)


def ping_server() -> bool:
    try:
        with socket.socket() as s:
            s.connect(("api.telegram.org", 443))
    except socket.error:
        return False
    return True


def main():
    if not ping_server():
        log.info("Waiting for connection...")
        while not ping_server():
            time.sleep(20)

    bot = Client(BOTNAME, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
    bot.set_parse_mode(ParseMode.HTML)

    users = Users(bot)
    config = Config(bot, users)
    cmds = Commands(bot, users, config)
    handlers = Handlers(users, config, cmds)

    log.info("Starting bot...")
    bot.start()
    log.info("Bot started.")

    bot.add_handler(MessageHandler(handlers.message))
    bot.add_handler(InlineQueryHandler(handlers.inline))
    bot.add_handler(CallbackQueryHandler(handlers.callback))

    config.log("Bot started.")

    log.info("Idling...")
    idle()

    config.log("Bot stopped.")

    log.info("Stopping...")
    bot.stop()
    log.info("Bot stopped.")

    sys.exit(0)


if __name__ == "__main__":
    main()
