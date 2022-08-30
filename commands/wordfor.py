import requests, json, html, urllib.parse
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

API = "https://reversedictionary.org/api/"
CREDITS_WEBSITE = "https://reversedictionary.org"
CREDITS = f'\n\n<i>From <a href="{CREDITS_WEBSITE}">Reverse Dictionary</a></i>.'

def function(LANG, definition: str, limit: int=1):
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

def command(LANG, bot, message):
	msg = message.reply_text(LANG('FETCHING_DATA'))
	d = (message.text or message.caption) if message.reply_to_message is None else None
	if not d:
		d = message.reply_to_message.text or message.reply_to_message.caption
	else:
		i = d.find(" ")
		if i == -1:
			d = None
		else:
			d = d[i+1:]
	if not d:
		msg.edit_text(LANG('PROVIDE_TEXT'))
	else:
		results = function(LANG, d)
		msg.edit_text(f'<b>{results[0]["word"].upper()}</b>: <i>{html.escape(d)}</i>\n\n{results[0]["desc"]}{CREDITS}')

def inlinequery(LANG, bot, inline, query):
	i = inline.query.find(" ")
	if i == -1:
		return [InlineQueryResultArticle(
			id = "0",
			title = "Reverse Dictionary",
			input_message_content = InputTextMessageContent(LANG('PROVIDE_SEARCH_QUERY')),
			description = LANG('PROVIDE_SEARCH_QUERY'),
		)]
	inline.query = inline.query[i+1:]
	results = function(inline.query, limit=7)
	return [InlineQueryResultArticle(
		id = r["word"],
		title = r["word"],
		input_message_content = InputTextMessageContent(f'<b>{r["word"].upper()}</b>: <i>{html.escape(inline.query)}</i>\n\n{r["desc"]}{CREDITS}'),
		description = r["desc"],
	) for r in results]