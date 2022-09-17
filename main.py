#!/usr/bin/env /usr/bin/python3

from variables import TOKEN, API_ID, API_HASH
from custom.log import log
from bot.config import Config
from bot.handlers import Handlers
from bot.users import Users
from commands import Commands

import sys, time, socket

from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler, InlineQueryHandler, CallbackQueryHandler
from pyrogram.enums import ParseMode

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

	bot = Client("dst212bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
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