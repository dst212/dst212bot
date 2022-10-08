import langs
from bot.classes import Command
from custom.misc import sender_is_admin, can_delete
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

class CmdSettings(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "settings"
		self.aliases = ["s"]

	def bool_button(self, LANG, m, callback, option):
		return InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, option) else "❌"} {LANG('SETTINGS_' + option.upper())}""", callback + option)

	def gen_markup(self, LANG, m):
		callback = f"{self.name} "
		lang = self.usr.get(m.chat.id, "lang")
		buttons = [
			[InlineKeyboardButton(LANG('CLOSE'), callback + "close")],
			[InlineKeyboardButton(f"""🌐 Language: {langs.flag(lang)}{langs.formal_name(lang)}""", callback + "lang")],
		]
		if m.chat.type == ChatType.PRIVATE:
			buttons.append([self.bool_button(LANG, m, callback, "override")])
		else:
			buttons.append([self.bool_button(LANG, m, callback, "auto-tr")])
		# let's keep sync-tr on by default forever
		# buttons.append([self.bool_button(LANG, m, callback, "sync-tr")])
		return InlineKeyboardMarkup(buttons)

	def callback(self, LANG, bot, c):
		m = c.callback.message
		chat = m.chat
		item = c.args[1] if len(c.args) > 1 else None
		value = c.args[2] if len(c.args) > 2 else None
		if sender_is_admin(c.callback):
			text, markup = None, None
			if item == "close":
				m.delete()
			elif item == "welcome" or (item == "start" and value is not None):
				if value is not None:
					self.usr.set(chat.id, "lang", value)
					LANG = langs.Lang(self.usr.lang_code(c.callback), self.cfg).string
				text = self.cmds["start"].welcome_message(LANG, c.callback.from_user)
				markup = self.cmds["start"].markup(LANG, c.callback.message.chat.id)
			elif item is not None:
				backbutton = f"{c.args[0]}"
				if item == "start":
					backbutton = f"{c.args[0]} welcome"
					item = "lang"
				option = self.usr.values.get(item)
				if option:
					old_value = self.usr.get(chat.id, item)
					if type(old_value) == bool:
						value = not old_value
					if value is not None:
						self.usr.set(chat.id, item, value)
						# LANG may have been changed
						if item == "lang":
							LANG = langs.Lang(self.usr.lang_code(c.callback), self.cfg).string
						text = LANG('SETTINGS_FOR_THIS_CHAT')
					elif option.options:
						if item == "lang":
							options = [[InlineKeyboardButton(f"{langs.flag(l)}{langs.formal_name(l)}", f"{c.text} {l}")] for l in option.options]
						else:
							options = [[InlineKeyboardButton(f"{i}", f"{c.text} {i}")] for i in option.options]
						markup = InlineKeyboardMarkup([[InlineKeyboardButton(LANG('BACK'), backbutton)]] + options)
						text = LANG('SETTINGS_SELECT_VALUE').format(item, old_value)
			else:
				text = LANG('SETTINGS_FOR_THIS_CHAT')
			if text:
				try:
					c.callback.edit_message_text(text, reply_markup=markup or self.gen_markup(LANG, m))
				except:
					pass
		else:
			c.callback.answer(LANG('MUST_BE_ADMIN'), show_alert=True)

	def run(self, LANG, bot, m):
		args = (m.text or m.caption).split(" ")
		if sender_is_admin(m):
			if len(args) > 1:
				if args[1] == "get":
					m.reply_document(f"{self.usr.base_dir}{m.chat.id}", file_name=f"{m.chat.id}.json")
				elif args[1] == "help":
					m.reply_text(LANG('SETTINGS_HELP'))
				elif args[1] == "set":
					m.reply_text(LANG('NOT_AVAILABLE_AT_THIS_TIME'))
				else:
					m.reply_text(LANG('INVALID_USAGE'))
			else:
				if can_delete(m):
					m.delete()
				bot.send_message(m.chat.id, LANG('SETTINGS_FOR_THIS_CHAT'), reply_markup=self.gen_markup(LANG, m))
		else:
			m.reply_text(LANG('MUST_BE_ADMIN'))
			# TODO: auto delete messages? nah