from bot.classes import Command
import logging
log = logging.getLogger(__name__)

import os, sys, json

class CmdAdmin(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "admin"

	def run(self, LANG, bot, m) -> None:
		out = ""
		args = (m.text or m.caption).split(" ")
		if self.cfg.is_admin(m):
			if len(args) > 2 and args[1] in ("test",):
				if args[2] in ("error", "explode"):
					raise Warning("This is a test.")
				elif args[2] in ("missing", "string"):
					out = LANG('string which doesn\'t exist')
			elif len(args) > 2 and args[1] in ("list",):
				l = self.cfg.get(args[2])
				if l and len(l) > 0:
					out = f"Items in <code>{args[2]}</code>:\n" + self.cfg.list_all(l)
				else:
					out = "No users in <code>" + args[2] + "</code>."
			elif len(args) > 2 and args[2] != "admin":
				items = args[3:] or [m.reply_to_message.id if m.reply_to_message else m.chat.id]
				if args[1] in ("add", "new"):
					out = self.cfg.add_items(args[2], items)
				elif args[1] in ("rem", "del", "remove", "delete"):
					out = self.cfg.rem_items(args[2], items)
			else:
				out = LANG('NO_PERMISSIONS')
		else:
			out = LANG('NO_PERMISSIONS')
		m.reply_text(out or LANG('INVALID_SYNTAX'))

class CmdReboot(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "reboot"

	def run(self, LANG, bot, m):
		if self.cfg.is_admin(m):
			m.reply_text(LANG('RESTARTING_BOT'))
			for i in self.cfg.get_log_chats():
				try:
					if i != m.chat.id:
						bot.forward_messages(i, m.chat.id, m.id)
						bot.send_message(i, f"[<code>{m.from_user.id if m.from_user else m.chat.id}</code>] Restarting...")
				except Exception as e:
					log.error(f"[{i}] {e}")
			log.info("Restarting the bot...")
			os.execl(sys.executable, sys.executable, *sys.argv)
		else:
			m.reply_text(LANG('LOL_NO_THANKS'))
