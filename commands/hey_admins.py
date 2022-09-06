from bot.classes import Command
from custom.log import log
from custom.misc import get_message_media, format_user

import requests, html
from pyrogram.enums import ChatType

class CmdHey(Command):
	def parse(self, bot, m) -> bool:
		if (
			m.from_user and
			m.reply_to_message and m.reply_to_message.text and
			m.reply_to_message.text[0] == "#" and
			m.chat.id in self.cfg.get_support_chats() and self.cfg.is_helper(m)
		):
			try:
				args = m.reply_to_message.text[1:].split("#")
				args[0], args[1] = int(args[0]), int(args[1])
				bot.copy_message(args[0], m.chat.id, m.id, reply_to_message_id=args[1])
				for i in self.cfg.get_support_chats():
					if i != m.chat.id:
						try:
							bot.send_message(i, format_user(m.from_user or m.sender_chat or m.chat) + f" in reply to <code>#{args[0]}</code><code>#{args[1]}#</code>")
							bot.forward_message(i, m.chat.id, m.id)
						except Exception as e:
							log.error(f"[{i}] {e}")
				return True
			except:
				pass
		return False

	def run(self, LANG, bot, m):
		sender = format_user(m.from_user or m.sender_chat)
		group = format_user(m.chat) if m.chat.type != ChatType.PRIVATE else None
		info_msg = f"<code>#{m.chat.id}</code><code>#{m.id}#</code>\n"
		info_msg += f"{group}, {sender}:" if group else f"{sender}:"
		for i in self.cfg.get_support_chats():
			try:
				bot.send_message(i, text=info_msg)
				if m.reply_to_message:
					bot.forward_messages(i, m.chat.id, m.reply_to_message.id)
				bot.forward_messages(i, m.chat.id, m.id)
			except Exception as e:
				log.error(f"[{i}] {e}")
