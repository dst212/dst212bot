from bot.classes import Command
import logging
log = logging.getLogger(__name__)
import langs
from custom.misc import command_entry
from pyrogram.enums import ChatType

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# /start
class CmdStart(Command):
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
class CmdHelp(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "help"
		self.args = ["[command]"]

	def help_buttons(self, LANG, bot, chat, m, cmds):
		if len(cmds) < 1:
			callback = f"help {chat} {m} "
			buttons = []
			row = []
			for k, _ in LANG('COMMANDS').items():
				row += [InlineKeyboardButton(k, callback + k)]
				if len(row) > 2:
					buttons += [row]
					row = []
			buttons += [row]
			bot.edit_message_text(chat, m, 
				f"<b>{LANG('HELP')}</b>" + "\n\n" + LANG('CHOOSE_A_BUTTON') + "\n\n" + LANG('INLINE_MODE_NOTICE'),
				reply_markup=InlineKeyboardMarkup(buttons)
			)
		else:
			cmd = self.cmds.get(cmds[0])
			bot.edit_message_text(chat, m,
				command_entry(LANG, cmd.name, {
					"args": cmd.args,
					"aliases": cmd.aliases,
					"desc": LANG('COMMANDS').get(cmd.name)
				}) + "\n\n" + LANG('INLINE_MODE_NOTICE'),
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(LANG('BACK'), f"help {chat} {m} /")]])
			)

	def run(self, LANG, bot, m):
		msg = bot.send_message(m.chat.id, LANG('LOADING'))
		self.help_buttons(LANG, bot, msg.chat.id, msg.id, (m.text or m.caption).split(" ")[1:])

	def callback(self, LANG, bot, c):
		if len(c.args) > 3:
			self.help_buttons(LANG, bot, int(c.args[1]), int(c.args[2]), [] if c.args[3] == "/" else [c.args[3]])

# /credits
class CmdCredits(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "credits"

	def run(self, LANG, bot, m):
		m.reply_text(LANG('CREDITS_MESSAGE'))
