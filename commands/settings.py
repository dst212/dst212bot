from bot.classes import Command
from custom.misc import sender_is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

class CmdSettings(Command):
	def gen_markup(self, m):
		callback = f"settings {m.chat.id} {m.id} "
		return InlineKeyboardMarkup([
			[InlineKeyboardButton(f"""🌐 Language: {self.usr.get(m.chat.id, "lang")}""", callback + "lang")],
			[InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, "override") else "❌"} {self.usr.lang(m, "SETTINGS_OVERRIDE")}""", callback + "override")],
			[InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, "sync-tr") else "❌"} {self.usr.lang(m, "SETTINGS_SYNC-TR")}""", callback + "sync-tr")],
		])

	def handle_callback(self, query, data):
		pass

	def run(self, LANG, bot, m):
		if sender_is_admin(m):
			m.reply_text(LANG("SETTINGS_FOR_THIS_CHAT"), reply_markup=self.gen_markup(m))
		else:
			m.reply_text(LANG("MUST_BE_ADMIN"))
			# TODO: auto delete messages? nah