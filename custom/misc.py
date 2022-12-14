from bot.classes import BaseCommand

import html, math

from pyrogram.types import Message, User, Chat, CallbackQuery
from pyrogram.enums import ChatType

def can_delete(m) -> bool:
	return m.chat.type == ChatType.PRIVATE or m.chat.get_member("me").privileges and m.chat.get_member("me").privileges.can_delete_messages

def sender_is_admin(m) -> bool:
	user = None
	if type(m) == CallbackQuery:
		user = m.from_user
		m = m.message
	else:
		user = m.from_user
	if m.chat.type == ChatType.PRIVATE:
		return True
	elif user is None:
		return False
	return m.chat.get_member(user.id).privileges is not None

def format_user(item) -> str:
	if type(item) == Chat:
		chat = item.title or item.first_name
		return f"""{f"<b>{html.escape(chat)}</b>" if chat else "Unknown chat"}{" (@" + item.username + ")" if item.username else ""} [<code>{item.id}</code>]"""
	elif type(item) == User:
		return f"""{item.mention("@" + item.username if item.username else html.escape(item.first_name))} [<code>{item.id}</code>]"""
	return f"Unknown ({item})"

def command_entry(LANG, cmd: BaseCommand, entry=None, inline_notice=True):
	return (
		f"""<code>/{cmd.name} {" ".join(cmd.args)}</code>\n""" +
		(LANG('ALIASES') + ": <code>/" + ("</code>, <code>/".join(cmd.aliases)) + "</code>\n" if cmd.aliases else "") + "\n" +
		(LANG('COMMANDS').get(cmd.name) or "") + ("\n\n" + LANG('INLINE_MODE_NOTICE') if inline_notice else "")
	) if cmd else LANG('NO_ENTRY_FOR').format(html.escape(entry)) if entry else LANG('NO_ENTRY')

def format_time(time) -> str:
	upt = math.floor(time)
	upt = [upt%60, upt//60, 0, 0]
	upt[1], upt[2] = upt[1]%60, upt[1]//60
	upt[2], upt[3] = upt[2]%24, upt[2]//24
	return (f"{upt[3]}d " if upt[3] else "") + (f"{upt[2]}h " if upt[2] or upt[3] else "") + (f"{upt[1]}m " if upt[1] or upt[2] or upt[3] else "") + f"{upt[0]}s"
