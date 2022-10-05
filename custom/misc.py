from bot.classes import Command
import html
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

def get_message_media(bot, message: Message):
	if not message.media:	return None, None
	elif message.audio:		return message.audio, bot.send_audio
	elif message.photo:		return message.photo, bot.send_photo
	elif message.video:		return message.video, bot.send_video
	elif message.voice:		return message.voice, bot.send_voice
	elif message.document:	return message.document, bot.send_document
	# TODO: sticker, animation, video_note, location, game, poll, dice
	return None, None

def format_user(item) -> str:
	if type(item) == Chat:
		chat = item.title or item.first_name
		return f"""{f"<b>{html.escape(chat)}</b>" if chat else "Unknown chat"}{" (@" + item.username + ")" if item.username else ""} [<code>{item.id}</code>]"""
	elif type(item) == User:
		return f"""{item.mention(" @" + item.username if item.username else html.escape(item.first_name))} [<code>{item.id}</code>]"""
	return f"Unknown ({item})"

def command_entry(LANG, cmd: Command, entry=None, inline_notice=True):
	return (
		f"""<code>/{cmd.name} {" ".join(cmd.args)}</code>\n""" +
		(LANG('ALIASES') + ": <code>/" + ("</code>, <code>/".join(cmd.aliases)) + "</code>\n" if cmd.aliases else "") + "\n" +
		(LANG('COMMANDS').get(cmd.name) or "") + ("\n\n" + LANG('INLINE_MODE_NOTICE') if inline_notice else "")
	) if cmd else LANG('NO_ENTRY_FOR').format(html.escape(entry)) if entry else LANG('NO_ENTRY')
