from bot.classes import Command
from .api import api_list, get_api, get_item, BASE_DIR
from .output import print_data

import os
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import ParseMode
from custom.find_matches import find_most_accurate

class CmdPokemon(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "pokemon"
		self.args = ["category", "name"]
		self.inline_args = ["category", "name"]
		self.aliases = ["p"]
		self.examples = ["pokemon eevee", "move quick attack"]

		self.available = ("pokemon", "move", "ability", "item")

	def get(self, LANG, query, category=None):
		title, text = "", ""
		if category: category = category.lower().replace("é","e").replace("è","e")
		if not category or category in self.available:
			categories = None
			data = get_api(category)
			title = " ".join(query)
			item = ("-".join(query)).lower()
			# data (a dictionary) is empty if the category is not valid (therefore a full search is performed)
			if not data:
				categories = {i: get_api(i) for i in self.available}
				for c, items in categories.items():
					if items.get(item):
						category = c
						break
			# if no category is set or category is valid but item is not found → find matches
			if not category or (data is not None and not data.get(item)):
				# selected keys() if category is valid else item → category if full search
				wordlist = data.keys() if category else {i: k for k, v in categories.items() for i in v.keys()}
				matches = find_most_accurate(wordlist, item)
				if len(matches) == 1:
					item = matches[0]
					title += " - " + LANG('DID_YOU_MEAN').format(item)
					if not category:
						category = wordlist[item]
				else:
					title = LANG('NO_RESULTS_FOR').format(title)
					text = "\n".join(matches)
			if text == "":
				text = print_data(LANG, item, category)
		else:
			text, title = LANG('IT_DOESNT_EXIST').format(args[1]), LANG('CATEGORY_DOESNT_EXIST')
		return text, "🔎 " + title

	def function(self, LANG, args):
		os.makedirs(BASE_DIR, exist_ok=True)
		if len(args) <= 1:
			return "- " + "\n- ".join(self.available), "Pokémon - " + LANG('AVAILABLE_CATEGORIES')
		elif len(args) > 2: # command category item[...]
			category = args[1]
			query = args[2:]
			return self.get(LANG, query, category)
		else: # command category
			if api_list().get(args[1]):
			# 	r = ""
			# 	for k, _ in get_api(args[1]).items():
			# 		r += "\n" + k
			# 	return r, LANG('RESULTS')
			# 	# or
				return LANG('PROVIDE_SEARCH_QUERY'), ""
			return self.get(LANG, args[1:])

	def run(self, LANG, bot, m):
		msg = m.reply_text(LANG('FETCHING_DATA'))
		res = self.function(LANG, (m.text or m.caption).split(" "))
		msg.edit_text(f"<b>{res[1]}</b>\n\n{res[0]}")

	def inline(self, LANG, bot, q):
		if len(q.args) < 2:
			return [InlineQueryResultArticle(
				id = "0",
				title = LANG('INVALID_SYNTAX'),
				input_message_content = InputTextMessageContent(LANG('PROVIDE_SEARCH_QUERY')),
				description = LANG('PROVIDE_SEARCH_QUERY'),
			)]
		else:
			output, result_title = self.function(LANG, q.args)
			return [InlineQueryResultArticle(
				id = "0",
				title = LANG('RESULTS_FOR').format(" ".join(q.args[2:])),
				input_message_content = InputTextMessageContent(output, parse_mode=ParseMode.HTML),
				description = result_title,
			)]