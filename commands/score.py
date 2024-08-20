from bot.classes import BaseCommand

import html
import json
import os
import re


class CmdScore(BaseCommand):
    name = "score"
    args = ["command", "arguments"]
    base_dir = "data/score/"

    def sort(self, data):
        data["items"] = {
            k: v
            for k, v in sorted(data["items"].items(), key=lambda x: x[1], reverse=True)
        }

    def score_str(self, lang, score):
        return f"<b>{html.escape(score["display"])}</b>\n\n" + (
            (
                "\n".join(
                    f"<i>{html.escape(k)}</i> : <code>{v}</code>"
                    for k, v in score["items"].items()
                )
                or lang.SCORE_NO_ITEMS
            )
        )

    async def get_score(self, m, name):
        cdir = f"{self.base_dir}{m.chat.id}/"
        os.makedirs(cdir, exist_ok=True)
        if not re.match("^[a-zA-Z0-9_-]+$", name):
            await m.reply(m.lang.SCORE_INVALID_NAME)
            return ""
        return cdir + name + ".json"

    async def score_get(self, m, score):
        file = await self.get_score(m, score)
        if not file:
            return
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return
        data = {}
        with open(file, "r") as f:
            data = json.load(f)
        await m.reply(self.score_str(m.lang, data))

    async def score_new(self, m, score):
        file = await self.get_score(m, score)
        if not file:
            return
        if os.path.exists(file):
            await m.reply(m.lang.SCORE_ALREADY_EXISTS.format(score))
            return
        data = {
            "display": score,
            "owner": m.from_user.id,
            "editors": [m.from_user.id],
            "items": {},
        }
        with open(file, "w") as f:
            json.dump(data, f)
        await m.reply(m.lang.SCORE_CREATED_SUCCESSFULLY.format(score))

    async def score_del(self, m, score):
        file = await self.get_score(m, score)
        if not file:
            return
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return
        data = {}
        with open(file, "r") as f:
            data = json.load(f)
            if not m.from_user.id == data["owner"]:
                await m.reply(m.lang.SCORE_YOU_ARENT_THE_OWNER)
                return
        os.remove(file)
        await m.reply(m.lang.SCORE_WAS_NOW_GONE.format(self.score_str(m.lang, data)))

    async def score_add(self, m, score, item, value=1):
        file = await self.get_score(m, score)
        if not file:
            return
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return
        data = {}
        with open(file) as f:
            data = json.load(f)
            if m.from_user.id not in data["editors"]:
                await m.reply(m.lang.SCORE_YOU_ARENT_AN_EDITOR)
                return
        if not data["items"].get(item):
            data["items"][item] = 0
        data["items"][item] += value
        self.sort(data)
        with open(file, "w") as f:
            json.dump(data, f)
        await m.reply(
            m.lang.SCORE_ITEM_SET_TO.format(
                html.escape(item), html.escape(data["display"]), data["items"][item]
            )
        )

    async def score_set(self, m, score, item, value=1):
        file = await self.get_score(m, score)
        if not file:
            return False
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return False
        data = {}
        with open(file) as f:
            data = json.load(f)
            if m.from_user.id not in data["editors"]:
                await m.reply(m.lang.SCORE_YOU_ARENT_AN_EDITOR)
                return False
        if data["items"].get(item) and value == 0:
            del data["items"][item]
        elif value != 0:
            data["items"][item] = value
            self.sort(data)
        with open(file, "w") as f:
            json.dump(data, f)
        if value != 0:
            await m.reply(
                m.lang.SCORE_ITEM_SET_TO.format(
                    html.escape(item), html.escape(data["display"]), data["items"][item]
                )
            )
        else:
            await m.reply(
                m.lang.SCORE_ITEM_DELETED.format(
                    html.escape(item), html.escape(data["display"])
                )
            )
        return True

    async def score_ren(self, m, score, newname):
        file = await self.get_score(m, score)
        newfile = await self.get_score(m, newname)
        if not file or not newfile:
            return
        with open(file, "r") as f:
            data = json.load(f)
            if not m.from_user.id == data["owner"]:
                await m.reply(m.lang.SCORE_YOU_ARENT_THE_OWNER)
                return
        os.rename(file, newfile)
        await m.reply(m.lang.SCORE_RENAMED_FROM.format(score, newname))

    async def score_display(self, m, score, display):
        file = await self.get_score(m, score)
        if not file:
            return
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return
        data = {}
        with open(file, "r") as f:
            data = json.load(f)
        if not m.from_user.id == data["owner"]:
            await m.reply(m.lang.SCORE_YOU_ARENT_THE_OWNER)
            return
        data["display"] = display
        with open(file, "w") as f:
            json.dump(data, f)
        await m.reply(m.lang.SCORE_DISPLAY_SET.format(score, html.escape(display)))

    async def score_setraw(self, m, score, items):
        file = await self.get_score(m, score)
        if not file:
            return
        if not os.path.exists(file):
            await m.reply(m.lang.SCORE_DOESNT_EXIST.format(score))
            return
        data = {}
        with open(file, "r") as f:
            data = json.load(f)
        if not m.from_user.id == data["owner"]:
            await m.reply(m.lang.SCORE_YOU_ARENT_THE_OWNER)
            return
        was = self.score_str(m.lang, data)
        data["items"] = items
        with open(file, "w") as f:
            json.dump(data, f)
        await m.reply(
            f"{m.lang.SCORE_WAS.format(was)}\n\n{m.lang.SCORE_NOW_ITS.format(self.score_str(m.lang, data))}"
        )

    async def run(self, bot, m):
        args = (m.text or m.caption).split(" ")
        if len(args) > 1:
            if args[1] in ("h", "help"):
                await m.reply(m.lang.SCORE_HELP)
            elif args[1] in ("get", "print"):
                if len(args) <= 2:
                    await m.reply(m.lang.SCORE_PROVIDE_NAME)
                elif len(args) > 3:
                    await m.reply(m.lang.SCORE_UNNEEDED_ARGUMENT)
                else:
                    await self.score_get(m, args[2])
            elif args[1] in ("new", "create"):
                if len(args) <= 2:
                    await m.reply(m.lang.SCORE_PROVIDE_NAME)
                elif len(args) > 3:
                    await m.reply(m.lang.SCORE_UNNEEDED_ARGUMENT)
                else:
                    await self.score_new(m, args[2])
            elif args[1] in ("del", "delete", "remove"):
                if len(args) <= 2:
                    await m.reply(m.lang.SCORE_PROVIDE_NAME)
                else:
                    for arg in args[2:]:
                        await self.score_del(m, arg)
            elif args[1] in ("ren", "rename"):
                if len(args) <= 3:
                    await m.reply(m.lang.SCORE_PROVIDE_NAME)
                else:
                    await self.score_ren(m, args[2], args[3])
            elif args[1] in ("display", "setdisplay"):
                if len(args) <= 3:
                    await m.reply(m.lang.SCORE_PROVIDE_NAME)
                else:
                    await self.score_display(m, args[2], " ".join(args[3:]))
            elif args[1] in ("add",):
                if len(args) <= 3:
                    await m.reply(f"{m.lang.USAGE}:\n{m.lang.SCORE_HELP_ADD}")
                else:
                    try:
                        await self.score_add(
                            m, args[2], args[3], int(args[4]) if len(args) > 4 else 1)
                    except ValueError:
                        await m.reply(m.lang.SCORE_ONLY_NUMBERS)
            elif args[1] in ("set",):
                if len(args) <= 3:
                    await m.reply(f"{m.lang.USAGE}:\n{m.lang.SCORE_HELP_SET}")
                else:
                    try:
                        await self.score_set(
                            m, args[2], args[3], int(args[4]) if len(args) > 4 else 1)
                    except ValueError:
                        await m.reply(m.lang.SCORE_ONLY_NUMBERS)
            elif args[1] in ("setraw",):
                i = args[2].find("\n") if len(args) > 2 else -1
                if i == -1:
                    await m.reply(f"{m.lang.USAGE}:\n{m.lang.SCORE_HELP_SETRAW}")
                else:
                    score = args[2][:i]
                    items = {}
                    try:
                        for item in (m.text or m.caption).split("\n")[1:]:
                            item = item.split(":")
                            if len(item) > 0 and item[0] != "":
                                items[item[0].strip()] = int(item[1]) if len(item) > 1 else 1
                        await self.score_setraw(m, score, items)
                    except ValueError:
                        await m.reply(m.lang.SCORE_ONLY_NUMBERS)
            elif args[1] in ("delitem",):
                if len(args) <= 3:
                    await m.reply(m.lang.SCORE_PROVIDE_ITEM_NAME)
                else:
                    await self.score_set(m, args[2], args[3], 0)
            else:
                await m.reply(m.lang.INVALID_SYNTAX)
        else:
            await m.reply(m.lang.SCORE_HELP)
