from bot.classes import BaseCommand
from custom.misc import format_user, format_time
from langs import Lang

import html, logging, os, re, sys, time, traceback
log = logging.getLogger(__name__)

from pyrogram.types import Chat
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import Forbidden

class CmdAdmin(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "admin"
		self.aliases = ["sudo"]

	def systeminfo(self, LANG, bot, m) -> str:
		out = "<b>.•°• System information •°•.</b>\n\n"
		# out += f"""Python path: <code>{html.escape(sys.executable)}</code>"""
		out += f"""<i>Python version</i> : <code>{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ({sys.implementation._multiarch})</code>\n"""
		out += f"""<i>Process</i> : <code>[</code><code>{self.cfg.p.pid}</code><code>] </code><code>{html.escape(" ".join(sys.argv))}</code>\n"""
		out += f"""<i>Memory</i> : <code>{round(self.cfg.p.memory_full_info().uss/1048576, 3)}MiB</code>\n"""
		out += "\n"
		out += f"""<i>Uptime</i> : <code>{format_time(time.time() - self.cfg.p.create_time())}</code>\n"""
		out += f"""<i>Running since {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.cfg.p.create_time()))}.</i>"""
		return out

	def run(self, LANG, bot, m) -> None:
		args = (m.text or m.caption).split(" ")
		if self.cfg.is_admin(m):
			if len(args) > 1:
				# reload config file
				if args[1] in ("reload", "refresh"):
					self.cfg.reload()
					m.reply_text(LANG('CONFIG_RELOADED'))
				# get system info
				elif args[1] in ("systeminfo", "sys"):
					m.reply_text(self.systeminfo(LANG, bot, m))
				# do some tests
				elif len(args) > 2 and args[1] in ("test",):
					if args[2] in ("error", "explode"):
						raise Warning("This is a test.")
					elif args[2] in ("missing", "string"):
						m.reply_text(LANG('string which doesn\'t exist'))
				# make the bot quit a group
				elif args[1] in ("leave", "quit"):
					self.leave(LANG, bot, m, args)
				# delete chat settings of someone
				elif args[1] in ("forget", "erase"):
					self.forget(LANG, bot, m, args)
				# broadcast a message wherever it's possible
				elif args[1] in ("broadcast", "spam"):
					self.broadcast(LANG, bot, m, args)
				# send a message to a specific chat
				elif len(args) > 2 and args[1] in ("send",):
					self.send(LANG, bot, m, args)
				# list chats/users in a specific group
				elif len(args) > 2 and args[1] in ("list", "get"):
					self.get(LANG, bot, m, args)
				# add a chat/user to a group
				elif len(args) > 2 and args[1] in ("add", "new"):
					items = args[3:] or [m.reply_to_message.id if m.reply_to_message else m.chat.id]
					m.reply_text(self.cfg.add_items(LANG, args[2], items))
				# remove a chat/user from a group
				elif len(args) > 2 and args[1] in ("rem", "del", "remove", "delete"):
					items = args[3:] or [m.reply_to_message.id if m.reply_to_message else m.chat.id]
					m.reply_text(self.cfg.rem_items(LANG, args[2], items))
				else:
					m.reply_text(LANG('INVALID_SYNTAX'))
			else:
				m.reply_text(LANG('INVALID_SYNTAX'))
		else:
			m.reply_text(LANG('NO_PERMISSIONS'))

	def get(self, LANG, bot, m, args):
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

	def send(self, LANG, bot, m, args):
		out = ""
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
			except Forbidden:
				out = LANG('ADMIN_I_CANT_WRITE_IN').format(format_user(chat))
			except Exception as e:
				out = html.escape(str(e))
			if sent:
				out = LANG('ADMIN_SENT_MESSAGE').format(format_user(sender), format_user(chat))
				self.cfg.log(out + ":", exclude=[m.chat.id], forward=[sent])
				out += "."
			m.reply_text(out, reply_to_message_id=m.id)

	def broadcast(self, LANG, bot, m, args):
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
				# commented the line below to avoid flood waits...
				# should fix this but it will take something like
				# a minute to send another message, it's probably not worth it
				# outm.edit_text(f"{i}/{len(chats)}")
				try:
					spam(chat.id)
					count += 1
				except Exception as e:
					log.warning(f"[{chat.id}] {e}")
				i += 1
			self.cfg.log(LANG('ADMIN_BROADCAST_MESSAGE').format(format_user(m.from_user), count, len(chats)))
			outm.delete()

	def byebye(self, bot, chat, me):
		use_chat_perm = not me.permissions and chat.permissions
		if (use_chat_perm and chat.permissions.can_send_other_messages) or (me.permissions and me.permissions.can_send_other_messages):
			my_job_is_done = "CAACAgQAAx0CWzSgSwACAu9jQbY6q1CWFVYmvd9oLvr9lTjDowADBAAC4VO0Gkg-S0vXzYliHgQ"
			swoosh = "CAACAgQAAx0CWzSgSwACAvBjQbY8ekRMaHdcyGcZbTjcuEpQvwACAgQAAuFTtBrgVhKngYV6YB4E"
			bot.send_sticker(chat.id, my_job_is_done)
			bot.send_sticker(chat.id, swoosh)
			return True
		elif (use_chat_perm and chat.permissions.can_send_messages) or (me.permissions and me.permissions.can_send_messages):
			LANG = Lang(self.usr.lang_code(chat.id), self.cfg).string
			bot.send_message(chat.id, LANG('MY_JOB_HERE_IS_DONE'))
			return True
		return False

	def leave(self, LANG, bot, m, args):
		self.cfg.log(LANG('ADMIN_SENT_THIS_COMMAND').format(format_user(m.from_user)), exclude=[m.chat.id], forward=[m])
		out = ""
		for i in args[2:] or [m.chat]:
			try:
				chat = i if type(i) == Chat else bot.get_chat(i)
				if chat.type == ChatType.PRIVATE:
					out += LANG('ADMIN_IS_PRIVATE_CHAT').format(format_user(chat))
				else:
					try:
						if not self.byebye(bot, chat, chat.get_member("me")):
							out += LANG('ADMIN_I_COULDNT_SAY_BYEBYE').format(format_user(chat)) + "\n"
						chat.leave()
						out += LANG('ADMIN_LEFT').format(format_user(chat))
					except:
						out += LANG('ADMIN_I_AM_NOT_A_MEMBER').format(format_user(chat))
			except Exception as e:
				log.warning(f"[{i}] {e}")
				traceback.print_exc()
				out += LANG('NOT_RECOGNIZED').format(f"[<code>{html.escape(str(i))}</code>]")
			out += "\n"
		if not out:
			out = LANG('NOTHING_CHANGED')
		self.cfg.log(out, exclude=[m.chat.id])
		# the chat removed may be this one, the fastest way to avoid this is a try-catc-, I mean, try-except
		try:
			m.reply_text(out)
		except:
			pass

	def forget(self, LANG, bot, m, args):
		self.cfg.log(LANG('ADMIN_SENT_THIS_COMMAND').format(format_user(m.from_user)), exclude=[m.chat.id], forward=[m])
		out = ""
		for i in args[2:] or [m.chat]:
			try:
				chat = i if type(i) == Chat else bot.get_chat(i)
				if self.usr.forget(chat.id):
					out += LANG('ADMIN_ERASED_SETTINGS_FOR').format(format_user(chat))
				else:
					out += LANG('ADMIN_NO_SETTINGS_TO_ERASE_FOR').format(format_user(chat))
			except:
				out += LANG('NOT_RECOGNIZED').format(f"[<code>{html.escape(str(i))}</code>]")
			out += "\n"
		if not out:
			out = LANG('NOTHING_CHANGED')
		self.cfg.log(out, exclude=[m.chat.id])
		m.reply_text(out)

class CmdReboot(BaseCommand):
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
