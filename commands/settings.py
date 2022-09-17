import langs
from bot.classes import Command
from custom.misc import sender_is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

class CmdSettings(Command):
	def gen_markup(self, m):
		callback = f"settings {m.chat.id} "
		lang = self.usr.get(m.chat.id, "lang")
		return InlineKeyboardMarkup([
			[InlineKeyboardButton(f"""🌐 Language: {langs.flag(lang)}{langs.formal_name(lang)}""", callback + "lang")],
			[InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, "override") else "❌"} {self.usr.lang(m, "SETTINGS_OVERRIDE")}""", callback + "override")],
			[InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, "sync-tr") else "❌"} {self.usr.lang(m, "SETTINGS_SYNC-TR")}""", callback + "sync-tr")],
		])

	def callback(self, LANG, bot, c):
		chat = bot.get_chat(int(c.args[1]))
		m = c.callback.message
		item = c.args[2] if len(c.args) > 2 else None
		value = c.args[3] if len(c.args) > 3 else None
		if sender_is_admin(c.callback):
			option = None if item is None else self.usr.values.get(item)
			if option:
				old_value = self.usr.get(chat.id, item)
				if type(old_value) == bool:
					self.usr.set(chat.id, item, not old_value)
				elif option.options:
					if value is None:
						markup = None
						if item == "lang":
							options = [[InlineKeyboardButton(f"{langs.flag(l)}{langs.formal_name(l)}", f"{c.callback.data} {l}")] for l in option.options]
						else:
							options = [[InlineKeyboardButton(f"{i}", f"{c.callback.data} {i}")] for i in option.options]
						c.callback.edit_message_text(
							LANG('SETTINGS_SELECT_VALUE').format(item, old_value),
							reply_markup=InlineKeyboardMarkup(
								[[InlineKeyboardButton(LANG('BACK'), f"settings {m.chat.id}")]] + options
							)
						)
						return
					else:
						self.usr.set(chat.id, item, value)
			try:
				c.callback.edit_message_text(LANG('SETTINGS_FOR_THIS_CHAT'), reply_markup=self.gen_markup(m))
			except:
				pass
		else:
			bot.answer_callback_query(c.callback.id, LANG('MUST_BE_ADMIN'), show_alert=True)

	def run(self, LANG, bot, m):
		if sender_is_admin(m):
			m.reply_text(LANG('SETTINGS_FOR_THIS_CHAT'), reply_markup=self.gen_markup(m))
		else:
			m.reply_text(LANG('MUST_BE_ADMIN'))
			# TODO: auto delete messages? nah