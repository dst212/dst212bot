from custom.misc import sender_is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

class Settings:
	def __init__(self, users):
		self.__usr = users

	def gen_markup(self, m):
		callback = f"settings.{m.chat.id}.{m.id}."
		return InlineKeyboardMarkup([
			[InlineKeyboardButton(f"""🌐 Language: {self.__usr.get(m.chat.id, "lang")}""", callback + "lang")],
			[InlineKeyboardButton(f"""{"✅" if self.__usr.get(m.chat.id, "override") else "❌"} {self.__usr.lang(m, "SETTINGS_OVERRIDE")}""", callback + "override")],
			[InlineKeyboardButton(f"""{"✅" if self.__usr.get(m.chat.id, "sync-tr") else "❌"} {self.__usr.lang(m, "SETTINGS_SYNC-TR")}""", callback + "sync-tr")],
		])

	def handle_callback(self, query, data):
		pass

	def command(self, bot, m):
		if sender_is_admin(m):
			m.reply_text(self.__usr.lang(m, "SETTINGS_FOR_THIS_CHAT"), reply_markup=self.gen_markup(m))
		else:
			m.reply_text(self.__usr.lang(m, "MUST_BE_ADMIN"))
			# TODO: auto delete messages? nah