from bot.classes import Command
import html, json
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, User, Chat, ChatPreview, InputMediaPhoto
from pyrogram.enums import UserStatus, ChatType

class CmdInfo(Command):
	def function(self, LANG, item) -> str:
		if type(item) == User:
			text = f"{LANG('INFO_FOR_TITLE').format(html.escape(item.first_name))}\n\n"
			if item.username: text += f"{LANG('INFO_USERNAME').format(item.username)}\n"
			text += f"{LANG('INFO_MENTION').format(item.mention())}\n"
			text += f"{LANG('INFO_ID').format(item.id)}\n"
			if item.dc_id: text += f"{LANG('INFO_DC').format(item.dc_id)}\n"
			if item.status:
				text += LANG('INFO_STATUS')
				if item.status == UserStatus.ONLINE: text += LANG('INFO_STATUS_ONLINE')
				elif item.status == UserStatus.OFFLINE: text += LANG('INFO_STATUSOFFLINE')
				elif item.status == UserStatus.RECENTLY: text += LANG('INFO_STATUS_RECENTLY')
				elif item.status == UserStatus.LAST_WEEK: text += LANG('INFO_STATUS_LAST_WEEK')
				elif item.status == UserStatus.LAST_MONTH: text += LANG('INFO_STATUS_LAST_MONTH')
				elif item.status == UserStatus.LONG_AGO: text += LANG('INFO_STATUS_LONG_AGO')
				else: text += LANG('UNKNOWN').lower()
				text += "\n"
			if item.language_code: text += f"{LANG('INFO_LANGUAGE_CODE').format(item.language_code)}\n"
			if item.is_verified: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_VERIFIED'))}.\n"
			if item.is_deleted: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_DELETED'))}.\n"
			if item.is_bot: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_BOT'))}.\n"
			if item.is_restricted: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_RESTRICTED'))}.\n"
			if item.is_scam: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_SCAM'))}.\n"
			if item.is_fake: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_FAKE'))}.\n"
			if item.is_support: text += f"{LANG('INFO_THIS_USER_IS').format(LANG('INFO_SUPPORT'))}.\n"
			if item.is_self: text += "\n" + LANG('INFO_ME')
		elif type(item) == Chat:
			text = f"{LANG('INFO_FOR_TITLE').format(html.escape(item.title or item.first_name))}\n"
			if item.bio: text += f"<i>{html.escape(item.bio)}</i>\n"
			if item.description: text += f"<i>{html.escape(item.description)}</i>\n"
			text += "\n"
			if item.members_count: text += f"{LANG('INFO_MEMBERS').format(item.members_count)}\n"
			if item.username: text += f"{LANG('INFO_USERNAME').format(item.username)}\n"
			if item.id: text += f"{LANG('INFO_ID').format(item.id)}\n"
			if item.dc_id: text += f"{LANG('INFO_DC').format(item.dc_id)}\n"
			if item.has_protected_content: text += f"{LANG('INFO_PROTECTED')}.\n"
			if item.is_verified: text += f"{LANG('INFO_THIS_CHAT_IS').format(LANG('INFO_VERIFIED'))}.\n"
			if item.is_scam: text += f"{LANG('INFO_THIS_CHAT_IS').format(LANG('INFO_SCAM'))}.\n"
			if item.is_fake: text += f"{LANG('INFO_THIS_CHAT_IS').format(LANG('INFO_FAKE'))}.\n"
			if item.is_restricted:
				text += f"{LANG('INFO_THIS_CHAT_IS').format('INFO_RESTRICTED')}:\n"
				for i in item.restrictions:
					text += f"- {i.text} ({i.platform})\n"
		return text

	def run(self, LANG, bot, m):
		if m.reply_to_message is not None:
			if m.reply_to_message.forward_from is not None:
				item = m.reply_to_message.forward_from
			else:
				item = m.reply_to_message.from_user
		else:
			args = (m.text or m.caption).split(" ")
			try:
				if len(args) == 1:
					item = m.from_user if m.chat.type == ChatType.PRIVATE else m.chat
				else:
					item = bot.get_users(args[1]) #[1:] if args[1][0] == "@" else int(args[1]))
			except:
				try:
					item = bot.get_chat(args[1])
				except:
					m.reply_text(f"{LANG('PROVIDE_USERNAME_OR_ID')}\n{LANG('EXAMPLE')}:\n/info @dst212bot")
					return

		text = self.function(LANG, item)

		photo = None
		if type(item) == Chat:
			#TODO: download the photo and re-upload it
			photo = None #if not item.photo else item.photo.big_file_id
		else: 
			photo = [i for i in bot.get_chat_photos(item.id, limit=1)],
			if len(photo) > 0 and len(photo[0]) > 0:
				photo = photo[0][0].file_id
			else:
				photo = None
		if photo:
			m.reply_media_group(media=[InputMediaPhoto(media=photo,caption=text)])
		else:
			m.reply_text(text)

	def inline(self, LANG, bot, q):
		try:
			item = bot.get_users(q.args[1]) #[1:] if q.args[1][0] == "@" else int(q.args[1]))
		except:
			return [InlineQueryResultArticle(
				title = LANG('PROVIDE_USERNAME_OR_ID'),
				input_message_content = InputTextMessageContent(LANG('PROVIDE_USERNAME_OR_ID')),
			)]
		text = self.function(LANG, item)
		return [InlineQueryResultArticle(
			title = f"{LANG('INFO_FOR')} {item.first_name}",
			input_message_content = InputTextMessageContent(text),
		)]