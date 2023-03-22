from bot.classes import BaseCommand
from custom.misc import command_entry
import langs

import logging
log = logging.getLogger(__name__)

from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# /start
class CmdStart(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "start"
		self.args = ["[command]"]

	def welcome_message(self, LANG, user):
		return (LANG('HI_THERE_ADMIN') if self.cfg.is_admin(user.id) else LANG('WELCOME_MESSAGE')).format(user.first_name)

	def markup(self, LANG, uid):
		lang = self.usr.lang_code(uid)
		return InlineKeyboardMarkup([
			[InlineKeyboardButton(f"""🌐 Language: {langs.flag(lang)}{langs.formal_name(lang)}""", f"settings start")]
		])

	def run(self, LANG, bot, m):
		if m.chat.type == ChatType.PRIVATE:
			m.reply_text(
				self.welcome_message(LANG, m.from_user),
				reply_markup=self.markup(LANG, m.chat.id)
			)
		else:
			m.reply_text(
				LANG('HI_THERE_USER').format(m.from_user.first_name),
				reply_markup=InlineKeyboardMarkup([
					[InlineKeyboardButton(LANG('LETS_START'), url=f"https://t.me/" + bot.get_users("me").username + "?start=start")]
				])
			)

# /help
class CmdHelp(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "help"
		self.args = ["[command]"]

	def help_buttons(self, LANG, bot, m, cmds):
		if len(cmds) < 1:
			callback = f"help "
			buttons = []
			row = []
			for k, _ in LANG('COMMANDS').items():
				row += [InlineKeyboardButton(k, callback + k)]
				if len(row) > 2:
					buttons += [row]
					row = []
			buttons += [row]
			m.edit_text(
				f"<b>{LANG('HELP')}</b>" + "\n\n" + LANG('CHOOSE_A_BUTTON') + "\n\n" + LANG('INLINE_MODE_NOTICE'),
				reply_markup=InlineKeyboardMarkup(buttons)
			)
		else:
			cmd = self.cmds.get(cmds[0])
			m.edit_text(
				command_entry(LANG, cmd, entry=cmds[0]),
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(LANG('BACK'), f"help /")]])
			)

	def run(self, LANG, bot, m):
		msg = bot.send_message(m.chat.id, LANG('LOADING'))
		self.help_buttons(LANG, bot, msg, (m.text or m.caption).split(" ")[1:])

	def callback(self, LANG, bot, c):
		self.help_buttons(LANG, bot, c.callback.message, [] if len(c.args) < 2 or c.args[1] == "/" else [c.args[1]])

# /credits
class CmdCredits(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "credits"

	def run(self, LANG, bot, m):
		m.reply_text(LANG('CREDITS_MESSAGE'))
