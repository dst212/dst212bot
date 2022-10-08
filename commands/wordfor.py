from bot.classes import BaseCommand

import html, json, requests, urllib.parse

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

API = "https://reversedictionary.org/api/"
CREDITS_WEBSITE = "https://reversedictionary.org"
CREDITS = f'\n\n<i>From <a href="{CREDITS_WEBSITE}">Reverse Dictionary</a></i>.'

class CmdWordFor(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "wordfor"
		self.args = ["definition"]
		self.inline_args = ["definition"]
		self.examples = ["the fear of high places"]

	def function(self, LANG, definition: str, limit: int=1):
		res = requests.get(API + "related?term=" + urllib.parse.quote(definition, safe=""))
		if res.status_code != 200:
			return LANG('WEBSITE_UNAVAILABLE'), LANG('IS_NOT_AVAILABLE_AT_THIS_TIME').format(CREDITS_WEBSITE)
		words = res.json()
		if len(words) == 0:
			return [{"word": definition, "desc": LANG('NO_RESULTS')}]
		results = []
		for w in words[:limit]:
			desc = requests.get(API + "define?term=" + w["word"])
			if desc.status_code == 200:
				desc = desc.text.strip()
			else:
				desc = LANG('IS_NOT_AVAILABLE_AT_THIS_TIME').format(CREDITS_WEBSITE)
			results += [{"word":w["word"], "desc": desc or "No description."}]
		return results

	def run(self, LANG, bot, m):
		msg = m.reply_text(LANG('FETCHING_DATA'))
		d = (m.text or m.caption) if m.reply_to_message is None else None
		if not d:
			d = m.reply_to_message.text or m.reply_to_message.caption
		else:
			i = d.find(" ")
			if i == -1:
				d = None
			else:
				d = d[i+1:]
		if not d:
			msg.edit_text(LANG('PROVIDE_TEXT'))
		else:
			results = self.function(LANG, d)
			msg.edit_text(f'<b>{results[0]["word"].upper()}</b>: <i>{html.escape(d)}</i>\n\n{results[0]["desc"]}{CREDITS}')

	def inline(self, LANG, bot, q):
		i = q.text.find(" ")
		if i == -1:
			return [InlineQueryResultArticle(
				id = "0",
				title = "Reverse Dictionary",
				input_message_content = InputTextMessageContent(LANG('PROVIDE_SEARCH_QUERY')),
				description = LANG('PROVIDE_SEARCH_QUERY'),
			)]
		text = q.text[i+1:]
		results = self.function(inline.query, limit=7)
		return [InlineQueryResultArticle(
			id = r["word"],
			title = r["word"],
			input_message_content = InputTextMessageContent(f'<b>{r["word"].upper()}</b>: <i>{html.escape(text)}</i>\n\n{r["desc"]}{CREDITS}'),
			description = r["desc"],
		) for r in results]
