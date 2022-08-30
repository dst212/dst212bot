import commands.pokemongo.rank as rank
import re
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

def function(LANG, args: list[str]):
	title = None
	if len(args) > 1:
		if args[1] in ("rank","r"):
			title, out = rank.get_rank(LANG, args[2:])
		elif args[1] in ("iv",):
			title, out = rank.get_iv(LANG, args[2:])
		else: #elif args[1] in ("h", "help"):
			out = LANG('POGO_HELP')
	else:
		out = LANG('POGO_HELP')
	return title, out or LANG('POGO_INVALID_USAGE')

def command(LANG, bot, message):
	args = (message.text or message.caption).split(" ")
	title, out = function(LANG, args)
	message.reply_text(f'<b>{title}</b>\n\n' + out if title else out)

def inlinequery(LANG, bot, inline, query):
	title, out = function(LANG, query)
	return [InlineQueryResultArticle(
		title = title or "Pokémon GO",
		input_message_content = InputTextMessageContent(f'<b>{title}</b>\n\n{out}'),
		description = re.sub("<[a-z/]*>","", out),
	)]