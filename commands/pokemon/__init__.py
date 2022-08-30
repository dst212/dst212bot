from .api import api_list, get_api, get_item, BASE_DIR
from .print import print_data

import os
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import ParseMode
from custom.find_matches import find_most_accurate

def function(LANG, args):
	os.makedirs(BASE_DIR, exist_ok=True)
	if len(args) <= 1:
		# r = ""
		# for k, _ in api_list().items():
		# 	r += "\n" + k
		# return r, LANG('RESULTS')
		return "- pokemon\n- move\n- ability\n- item", "Pokémon - " + LANG('AVAILABLE_CATEGORIES')
	elif len(args) <= 2: # command category
		link = api_list().get(args[1])
		if link is None:
			return LANG('NO_RESULTS_FOR').format(args[1]), LANG('NO_RESULTS')
		else:
			r = ""
			for k, _ in get_api(args[1]).items():
				r += "\n" + k
			return r, LANG('RESULTS')
	else: # command category item[...]
		image, data, link = None, None, None
		title, text, item = "", "", ""
		category = args[1]
		if category in api_list(): # category is valid, else full search
			title = " ".join(args[2:])
			data = get_api(args[1])
			item = ("-".join(args[2:])).lower() #.replace(".", "-")
			link = data.get(item)
			if link is None: # if no results, look for similar results
				matches = find_most_accurate([k for k,_ in data.items()], item)
				if len(matches) == 1:
					item = matches[0]
					title += " - " + LANG('DID_YOU_MEAN').format(item)
				else:
					title = LANG('NO_RESULTS_FOR').format(title)
					text = "\n".join(matches)
			if text == "":
				text = print_data(LANG, item, category)
			return text, title
		else:
			# TODO: full search
			return LANG('IT_DOESNT_EXIST').format(args[1]), LANG('CATEGORY_DOESNT_EXIST')

def command(LANG, bot, message) -> None:
	msg = message.reply_text(LANG('FETCHING_DATA'))
	res = function(LANG, (message.text or message.caption).split(" "))
	msg.edit_text(f"<b>{res[1]}</b>\n\n{res[0]}")

def inlinequery(LANG, bot, inline, query):
	if len(query) < 2:
		return [InlineQueryResultArticle(
			id = "0",
			title = LANG('INVALID_SYNTAX'),
			input_message_content = InputTextMessageContent(LANG('PROVIDE_SEARCH_QUERY')),
			description = LANG('PROVIDE_SEARCH_QUERY'),
		)]
	else:
		output, result_title = function(LANG, query)
		return [InlineQueryResultArticle(
			id = "0",
			title = LANG('RESULTS_FOR').format(" ".join(query)),
			input_message_content = InputTextMessageContent(output, parse_mode=ParseMode.HTML),
			description = result_title,
		)]