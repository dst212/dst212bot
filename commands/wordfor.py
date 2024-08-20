from bot.classes import BaseCommand
from misc.fun import quick_answer

import asyncio
import html
import requests
import urllib.parse

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

API = "https://reversedictionary.org/api/"
CREDITS_WEBSITE = "https://reversedictionary.org"
CREDITS = f"\n\n<i>From <a href=\"{CREDITS_WEBSITE}\">Reverse Dictionary</a></i>."


class CmdWordFor(BaseCommand):
    name = "wordfor"
    args = ["definition"]
    inline_args = ["definition"]
    examples = ["the fear of high places"]

    async def function(self, lang, definition: str, limit: int = 1):
        res = await asyncio.to_thread(
            requests.get,
            f"{API}related?term={urllib.parse.quote(definition, safe="")}"
        )
        if res.status_code != 200:
            return lang.WEBSITE_UNAVAILABLE, lang.IS_NOT_AVAILABLE_AT_THIS_TIME.format(CREDITS_WEBSITE)
        words = res.json()
        if len(words) == 0:
            return [{"word": definition, "desc": lang.NO_RESULTS}]
        results = []
        for w in words[:limit]:
            desc = await asyncio.to_thread(requests.get, f"{API}define?term={w["word"]}")
            if desc.status_code == 200:
                desc = desc.text.strip()
            else:
                desc = lang.IS_NOT_AVAILABLE_AT_THIS_TIME.format(CREDITS_WEBSITE)
            results += [{"word": w["word"], "desc": desc or "No description."}]
        return results

    async def run(self, bot, m):
        r = await m.reply(m.lang.FETCHING_DATA)
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
            await r.edit(m.lang.PROVIDE_TEXT)
        else:
            results = await self.function(m.lang, d)
            await r.edit(
                f"<b>{results[0]["word"].upper()}</b>: <i>{html.escape(d)}</i>\n\n{results[0]["desc"]}{CREDITS}"
            )

    async def inline(self, bot, q):
        i = q.query.find(" ")
        if i == -1:
            await quick_answer(q, q.lang.PROVIDE_SEARCH_QUERY, "h_wordfor")
            return
        text = q.query[i+1:]
        results = await self.function(q.lang, text, limit=7)
        await q.answer([
            InlineQueryResultArticle(
                id=r["word"],
                title=r["word"],
                input_message_content=InputTextMessageContent(
                    f"<b>{r["word"].upper()}</b>: <i>{html.escape(text)}</i>\n\n{r["desc"]}{CREDITS}"
                ),
                description=r["desc"],
            )
            for r in results
        ], cache_time=self.cache_time)
