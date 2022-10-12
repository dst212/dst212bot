from bot.classes import BaseCommand
from custom.misc import sender_is_admin, can_delete
import langs

import html

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified

class CmdSettings(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "settings"
		self.aliases = ["s"]

	def button(self, LANG, m, callback, option_name: str):
		return InlineKeyboardButton(f"""{LANG('SETTINGS_' + option_name.upper())}: {self.usr.get(m.chat.id, option_name)}""", callback + option_name)

	def bool_button(self, LANG, m, callback, option_name: str):
		return InlineKeyboardButton(f"""{"✅" if self.usr.get(m.chat.id, option_name) else "❌"} {LANG('SETTINGS_' + option_name.upper())}""", callback + option_name)

	def list_buttons(self, LANG, m, callback, option, start: int=0, step: int=5, back_button: str=None, current_value=None):
		last_page = len(option.options) - ((len(option.options) - 1) % step + 1)
		return InlineKeyboardMarkup(
			[[InlineKeyboardButton(LANG('BACK'), back_button or self.name)]] + [[ #first_row + [[
				InlineKeyboardButton(f"""{"✅ " if i == current_value else ""}{option.options.get(i)}""", f"{callback} set {i}")
			] for i in list(option.options.keys())[start:start+step]] + ([[
				InlineKeyboardButton("⏪", f"{callback} page 0"),
				InlineKeyboardButton("◀", f"{callback} page {max(start-step, 0)}"),
				InlineKeyboardButton("▶", f"{callback} page {min(start+step, last_page)}"),
				InlineKeyboardButton("⏩", f"{callback} page {last_page}"),
			]] if last_page != 0 else [])
		)

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
			buttons.append([self.button(LANG, m, callback, "auto-tr")]) 
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
			# show main menu of settings
			if item is None:
				text = LANG('SETTINGS_FOR_THIS_CHAT')
			# delete the settings message
			elif item == "close":
				m.delete()
			# settings in the start message
			elif item == "welcome" or (item == "start" and value is not None):
				if value is not None:
					self.usr.set(chat.id, "lang", value)
					LANG = langs.Lang(self.usr.lang_code(c.callback), self.cfg).string
				text = self.cmds["start"].welcome_message(LANG, c.callback.from_user)
				markup = self.cmds["start"].markup(LANG, c.callback.message.chat.id)
			# set value
			else:
				back_button = f"{c.args[0]}"
				if item == "start":
					back_button = f"{c.args[0]} welcome"
					item = "lang"
				option = self.usr.values.get(item)
				if option:
					current_value = self.usr.get(chat.id, item)
					if option.type == bool:
						value = not current_value
					# set value usually for option with multiple possible values
					elif value == "set":
						value = c.args[3] if len(c.args) > 3 else None
					# browse pages of multiple values
					elif value == "page":
						value = None
					# change the option's value
					if value is not None:
						self.usr.set(chat.id, item, value)
						# LANG may have been changed
						if item == "lang":
							LANG = langs.Lang(self.usr.lang_code(c.callback), self.cfg).string
						text = LANG('SETTINGS_FOR_THIS_CHAT')
					# list available options
					elif option.options:
						start = int(c.args[3]) if len(c.args) > 3 else 0
						markup = self.list_buttons(LANG, m, " ".join(c.args[:2]), option, start=start, back_button=back_button, current_value=current_value)
						text = LANG('SETTINGS_SELECT_VALUE').format(item, current_value)
			try:
				if text:
					c.callback.edit_message_text(text, reply_markup=markup or self.gen_markup(LANG, m))
				elif markup:
					c.callback.edit_message_reply_markup(markup)
			except MessageNotModified:
				c.callback.answer(LANG('NOTHING_CHANGED'))
		else:
			c.callback.answer(LANG('MUST_BE_ADMIN'), show_alert=True)

	def run(self, LANG, bot, m):
		args = (m.text or m.caption).split(" ")
		if sender_is_admin(m):
			if len(args) > 1:
				if args[1] == "help":
					m.reply_text(LANG('SETTINGS_HELP'))
				elif args[1] == "get":
					m.reply_document(f"{self.usr.base_dir}{m.chat.id}", file_name=f"{m.chat.id}.json")
				elif args[1] == "set":
					if len(args) > 3:
						item = args[2]
						value = args[3]
						option = self.usr.values.get(item)
						if option:
							old_value = self.usr.get(m.chat.id, item)
							if option.type == bool:
								if value.lower() in ("on", "true", "enable"):
									value = True
								else:
									value = False
							if option.is_valid(value):
								if self.usr.set(m.chat.id, item, option.type(value)):
									m.reply_text(LANG('SETTINGS_SET_TO').format(item, self.usr.get(m.chat.id, item), old_value))
								else:
									m.reply_text(LANG('SETTINGS_COULD_NOT_SET').format(item, self.usr.get(m.chat.id, item), old_value))
							else:
								m.reply_text(LANG('SETTINGS_NOT_VALID_VALUE_FOR').format(html.escape(value), item))
						else:
							m.reply_text(LANG('NOT_RECOGNIZED').format(f"<code>{html.escape(item)}</code>"))
					else:
						m.reply_text(LANG('SYNTAX') + f":\n<code>/{self.name} set &lt;item&gt; &lt;value&gt;</code>")
				else:
					m.reply_text(LANG('INVALID_USAGE'))
			else:
				if can_delete(m):
					m.delete()
				bot.send_message(m.chat.id, LANG('SETTINGS_FOR_THIS_CHAT'), reply_markup=self.gen_markup(LANG, m))
		else:
			m.reply_text(LANG('MUST_BE_ADMIN'))
			# TODO: auto delete messages? nah
