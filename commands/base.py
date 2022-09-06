from bot.classes import Command
from custom.log import log
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def command_entry(LANG, k, v):
	return (
		f"""<code>/{k} {" ".join(item for item in v["args"])}</code>\n""" +
		(LANG('ALIASES') + ": <code>/" + ("</code>, <code>/".join(item for item in v["aliases"])) + "</code>\n" if v.get("aliases") else "") +
		"\n" + v["desc"]
	) if v else LANG('NO_ENTRY_FOR').format(k)

def help_buttons(LANG, bot, chat, m, cmds):
	# TODO: pass message and edit __usr.lang
	if len(cmds) < 1:
		callback = f"help.{chat}.{m}."
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
		bot.edit_message_text(chat, m,
			command_entry(LANG, cmds[0], LANG('COMMANDS').get(cmds[0])) + "\n\n" + LANG('INLINE_MODE_NOTICE'),
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(LANG('BACK'), f"help.{chat}.{m}./")]])
		)

class CmdStart(Command):
	def run(self, LANG, bot, m):
		m.reply_text(LANG('WELCOME_MESSAGE').format(m.from_user.first_name))

class CmdHelp(Command):
	def run(self, LANG, bot, m):
		m = bot.send_message(m.chat.id, LANG('LOADING'))
		help_buttons(LANG, bot, m.chat.id, m.id, (m.text or m.caption).split(" ")[1:])

class CmdCredits(Command):
	def run(self, LANG, bot, m):
		m.reply_text(LANG('CREDITS_MESSAGE'))
