from bot.classes import Command
import html, json
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, User, Chat, ChatPreview, InputMediaPhoto
from pyrogram.enums import UserStatus, ChatType

class CmdInfo(Command):
	def function(self, LANG, item) -> str:
		if type(item) == User:
			text = f"<i>Info for <u>{html.escape(item.first_name)}</u></i>\n\n"
			if item.username: text += f"<b>Username</b>: @{item.username}\n"
			text += f"<b>Mention</b>: {item.mention()}\n" #f"<a href=\"tg://user?id={item.id}\">{html.escape(item.first_name)}</a>\n"
			text += f"<b>ID</b>: <code>{item.id}</code>\n"
			if item.dc_id: text += f"<b>DC</b>: {item.dc_id}\n"
			if item.status:
				text += f"<b>Status</b>: "
				if item.status == UserStatus.ONLINE: text += "online"
				elif item.status == UserStatus.OFFLINE: text += "offline"
				elif item.status == UserStatus.RECENTLY: text += "last seen recently"
				elif item.status == UserStatus.LAST_WEEK: text += "last seen within a week"
				elif item.status == UserStatus.LAST_MONTH: text += "last seen within a month"
				elif item.status == UserStatus.LONG_AGO: text += "last seen a long time ago"
				else: text += "unknown"
				text += "\n" 
			if item.language_code: text += f"<b>Language code</b>: {item.language_code}\n"
			if item.is_verified: text += "This user is verified.\n" 
			if item.is_deleted: text += "This user is deleted.\n" 
			if item.is_bot: text += "This user is a bot.\n" 
			if item.is_restricted: text += "This user is restricted.\n" 
			if item.is_scam: text += "This user is marked as <b>scam</b>.\n" 
			if item.is_fake: text += "This user is fake.\n" 
			if item.is_support: text += "This user is support.\n"
			if item.is_self: text += "\nWait... That's me?"
		elif type(item) == Chat:
			text = f"<i>Info for <u>{html.escape(item.title or item.first_name)}</u></i>\n"
			if item.bio: text += f"<i>{html.escape(item.bio)}</i>\n"
			if item.description: text += f"<i>{html.escape(item.description)}</i>\n"
			text += "\n"
			if item.members_count: text += f"<b>Members</b>: {item.members_count}\n"
			if item.username: text += f"<b>Username</b>: @{item.username}\n"
			if item.id: text += f"<b>ID</b>: <code>{item.id}</code>\n"
			if item.dc_id: text += f"<b>DC</b>: {item.dc_id}\n"
			if item.has_protected_content: text += "This chat has its content protected.\n"
			if item.is_verified: text += "This chat is verified.\n"
			if item.is_scam: text += "This chat is scam.\n"
			if item.is_fake: text += "This chat is fake.\n"
			if item.is_restricted:
				text += "This chat is restricted:\n"
				for i in item.restrictions:
					text += f"- {i.text} ({i.platform})"
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
			title = f"Info for {item.first_name}",
			input_message_content = InputTextMessageContent(text),
		)]