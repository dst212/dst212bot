#!/usr/bin/env /usr/bin/python3

from variables import TOKEN as TOKEN, API_ID, API_HASH
from custom.log import log
from langs import en as LANG
from bot.config import Config
from bot.handlers import Handlers
from bot.users import Users
from commands import Commands

import os, sys, time

from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler, InlineQueryHandler, CallbackQueryHandler
from pyrogram.enums import ParseMode

###############################################################################

# def print_info(bot, message):
# 	group = "" if message.chat.username == message.from_user.username else f"@{message.chat.username or ''}[{message.chat.id}], "
# 	log.info(
# 		f"[{message.date.strftime('%Y-%m-%d %H:%M:%S')}] " +
# 		group + f"@{(message.from_user or message.sender_chat).username}[{(message.from_user or message.sender_chat).id}]: " +
# 		(message.text or message.caption or "[media]")
# 	)

def main():
	while os.system("ping -c 1 api.telegram.org>/dev/null") != 0:
		log.info("Waiting for connection...")
		time.sleep(20)

	bot = Client("dst212bot testing", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
	bot.set_parse_mode(ParseMode.HTML)

	users = Users(bot)
	config = Config(bot, users)
	cmds = Commands(bot, users, config)
	handlers = Handlers(users, config, cmds)

	log.info("Starting bot...")
	bot.start()
	log.info("Bot started.")

	bot.add_handler(MessageHandler(handlers.handle_update))
	bot.add_handler(InlineQueryHandler(handlers.inlinequery))
	bot.add_handler(CallbackQueryHandler(handlers.handle_callback))

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