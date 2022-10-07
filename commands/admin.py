from bot.classes import Command
from custom.misc import format_user
import logging, re, os, sys, html
log = logging.getLogger(__name__)

from pyrogram.types import Chat

class CmdAdmin(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "admin"
		self.alias = "sudo"

	def run(self, LANG, bot, m) -> None:
		args = (m.text or m.caption).split(" ")
		if self.cfg.is_admin(m):
			if len(args) > 2 and args[1] in ("test",):
				if args[2] in ("error", "explode"):
					raise Warning("This is a test.")
				elif args[2] in ("missing", "string"):
					m.reply_text(LANG('string which doesn\'t exist'))
			elif len(args) > 2 and args[1] in ("list",):
				out = ""
				outm = m.reply_text(LANG('LOADING'))
				if args[2] == "chats":
					chats = self.usr.get_active_chats()
					# out = "\n".join([f"{k}\n - " + "\n - ".join([format_user(u) for u in v.values()]) for k, v in chats.items() if type(v) == dict])
					out = "\n".join([f"{k}: {len(v)}" for k, v in chats.items() if type(v) == dict]) + f"\n\n{LANG('TOTAL')}: {chats['count']}"
				else:
					l = self.cfg.get(args[2])
					if l and len(l) > 0:
						out = LANG('ADMIN_ITEMS_IN').format(args[2]) + self.cfg.list_all(l)
					else:
						out = LANG('ADMIN_NO_ITEMS_IN').format(args[2])
				outm.edit_text(out)
			elif len(args) > 2 and args[1] in ("add", "new"):
				items = args[3:] or [m.reply_to_message.id if m.reply_to_message else m.chat.id]
				m.reply_text(self.cfg.add_items(LANG, args[2], items))
			elif len(args) > 2 and args[1] in ("rem", "del", "remove", "delete"):
				items = args[3:] or [m.reply_to_message.id if m.reply_to_message else m.chat.id]
				m.reply_text(self.cfg.rem_items(LANG, args[2], items))
			elif len(args) > 2 and args[1] in ("send",):
				reply_id = None
				chat = re.split("[\.\#]", args[2])
				try: chat, reply_id = bot.get_chat(int(chat[0]) if chat[0].isnumeric() else chat[0]), chat[1] if len(chat) > 1 else None
				except: pass
				sent, sender = None, None
				if type(chat) != Chat:
					out = LANG('ADMIN_NOT_JOINED_OR_INVALID')
				elif reply_id and not reply_id.isnumeric():
					out = LANG('ADMIN_MESSAGE_ID_MUST_BE_INTEGER')
				else:
					reply_id = reply_id and int(reply_id)
					sender = m.from_user
					try:
						if m.reply_to_message:
							m = m.reply_to_message # so that the output message will reply to the forwarded message
							sent = m.copy(chat.id, reply_to_message_id=reply_id)
						else:
							text = " ".join(args[3:]) # not escaped on purpose
							if text:
								sent = bot.send_message(chat.id, text, reply_to_message_id=reply_id)
							else:
								out = LANG('PROVIDE_TEXT')
					except Exception as e:
						out = html.escape(str(e))
					if sent:
						out = LANG('ADMIN_SENT_MESSAGE').format(format_user(sender), format_user(chat))
						self.cfg.log(out + ":", exclude=[m.chat.id], forward=[sent])
						out += "."
					m.reply_text(out + ".", reply_to_message_id=m.id)
			elif len(args) > 1 and args[1] in ("broadcast", "spam"):
				outm = m.reply_text(LANG('LOADING'))
				spam = None # will be a lambda function
				chats = self.usr.get_active_chats_list()
				count = 0
				if m.reply_to_message:
					spam = lambda chat : m.reply_to_message.copy(chat)
				else:
					text = " ".join(args[2:])
					if text:
						spam = lambda chat : bot.send_message(chat, text)
					else:
						outm.edit_text(LANG('PROVIDE_TEXT'))
				if spam:
					i = 0
					for chat in chats:
						outm.edit_text(f"{i}/{len(chats)}")
						try:
							spam(chat.id)
							count += 1
						except Exception as e:
							log.warning(f"[{chat.id}] {e}")
						i += 1
					outm.delete()
					self.cfg.log(LANG('ADMIN_BROADCAST_MESSAGE').format(format_user(m.from_user), count, len(chats)))
			else:
				m.reply_text(LANG('INVALID_SYNTAX'))
		else:
			m.reply_text(LANG('NO_PERMISSIONS'))

class CmdReboot(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "reboot"

	def run(self, LANG, bot, m):
		if self.cfg.is_admin(m):
			m.reply_text(LANG('RESTARTING_BOT'))
			self.cfg.log(LANG('ADMIN_RESTARTING').format(m.from_user.id if m.from_user else m.chat.id), forward=[m], exclude=[m.chat.id])
			log.info("Restarting the bot...")
			os.execl(sys.executable, sys.executable, *sys.argv)
		else:
			m.reply_text(LANG('LOL_NO_THANKS'))
