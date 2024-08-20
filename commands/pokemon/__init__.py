from bot.classes import BaseCommand
from .api import get_api, BASE_DIR
from .output import print_data
from misc.fun import quick_answer

import html
import os

from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import ParseMode
from custom import find_most_accurate


class CmdPokemon(BaseCommand):
    name = "pokemon"
    args = ["category", "name"]
    inline_args = ["category", "name"]
    aliases = ["pkm", "pkmn"]
    examples = ["pokemon eevee", "move quick attack"]

    available = ("pokemon", "move", "ability", "item")

    def get(self, lang, query, category=None):
        title, text = "", ""
        if category:
            category = category.lower().replace("é", "e").replace("è", "e")
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
                wordlist = (
                    data.keys()
                    if category
                    else {i: k for k, v in categories.items() for i in v.keys()}
                )
                matches = find_most_accurate(wordlist, item)
                if len(matches) == 1:
                    item = matches[0]
                    title += f" - {lang.DID_YOU_MEAN.format(html.escape(item))}"
                    if not category:
                        category = wordlist[item]
                else:
                    title = lang.NO_RESULTS_FOR.format(title)
                    text = "\n".join(matches)
            if text == "":
                text = print_data(lang, item, category)
        else:
            text, title = lang.IT_DOESNT_EXIST.format(html.escape(category)), lang.CATEGORY_DOESNT_EXIST
        return text, f"🔎 {title}"

    def function(self, lang, args):
        os.makedirs(BASE_DIR, exist_ok=True)
        if len(args) <= 1:
            return f"- {"\n- ".join(self.available)}", f"Pokémon - {lang.AVAILABLE_CATEGORIES}"
        else:
            if args[1] in self.available:
                if len(args) <= 2:
                    return lang.PROVIDE_SEARCH_QUERY, ""
                return self.get(lang, args[2:], args[1])
            return self.get(lang, args[1:])

    async def run(self, bot, m):
        r = await m.reply(m.lang.FETCHING_DATA)
        res = self.function(m.lang, (m.text or m.caption).split(" "))
        await r.edit(f"<b>{res[1]}</b>\n\n{res[0]}")

    async def inline(self, bot, q):
        args = q.query.split(" ")
        if len(args) < 2:
            await quick_answer(q, q.lang.PROVIDE_SEARCH_QUERY, "h_pokemon")
        else:
            output, result_title = self.function(q.lang, args)
            await q.answer([
                InlineQueryResultArticle(
                    title=q.lang.RESULTS_FOR.format(html.escape(" ".join(args[2:]))),
                    input_message_content=InputTextMessageContent(
                        output, parse_mode=ParseMode.HTML),
                    description=result_title,
                )
            ], cache_time=self.cache_time)
