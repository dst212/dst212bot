from bot.classes import BaseCommand

import asyncio
import html
import json
import logging
import os
import re

log = logging.getLogger(__name__)


class CmdCounter(BaseCommand):
    name = "counter"
    args = ["command", "arguments"]
    base_dir = "./data/counter/"
    groups = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = asyncio.Lock()
        asyncio.run_coroutine_threadsafe(self.load_all(), asyncio.get_event_loop())

    def is_valid_name(self, name: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))

    def update_group(self, chat, counter, data):
        g = self.groups.get(chat)
        if g and g.get(counter):
            g[counter] = data
            self.save(chat, counter, data)

    def save(self, chat, counter, data) -> bool:
        if self.is_valid_name(counter):
            path = f"{self.base_dir}{chat}/"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}{counter}", "w") as f:
                json.dump(data, f)
            return True
        return False

    def load(self, chat_id: int, counter) -> dict:
        ret = None
        path = f"{self.base_dir}{chat_id}/{counter}"
        if self.is_valid_name(counter) and os.path.exists(path):
            with open(path, "r") as f:
                ret = json.load(f)
            if ret["triggers"]:
                log.info(f"Counter loaded: {counter}")
                if not self.groups.get(chat_id):
                    self.groups[chat_id] = {}
                self.groups[chat_id][counter] = ret
        return ret

    async def load_all(self):
        async with self.lock:
            os.makedirs(self.base_dir, exist_ok=True)
            for chat in os.listdir(self.base_dir):
                if re.match(r"^(-|)[0-9]+$", chat):
                    chat = int(chat)
                    for counter in os.listdir(f"{self.base_dir}{chat}"):
                        self.load(chat, counter)
            log.info(
                f"Loaded {len(self.group)} groups"
                f" ({sum(len(i) for i in self.group.values())} total counters).")

    async def get(self, m, counter):
        data = self.load(m.chat.id, counter)
        await m.reply(
            m.lang.COUNTER_IS.format(
                html.escape(data["display"]), data["value"]
            ) if data else
            m.lang.COUNTER_DOESNT_EXIST.format(counter)
        )

    async def parse_message(self, m):
        text = m.text or m.caption
        if text:
            text = text.lower()
            async with self.lock:
                group = self.groups.get(m.chat.id)
                if group:
                    for k, v in group.items():
                        saved = True
                        for word in v["triggers"]:
                            if word in text:
                                saved = False
                                group[k]["value"] += v["step"]
                                await m.reply(
                                    m.lang.COUNTER_SET.format(
                                        html.escape(v["display"]), v["value"]))
                        if not saved:
                            self.save(m.chat.id, k, v)

    async def new(self, m, counter):
        if os.path.exists(f"{self.base_dir}{m.chat.id}/{counter}"):
            await m.reply(m.lang.COUNTER_ALREADY_EXISTS)
        elif not self.save(
            m.chat.id,
            counter,
            {
                "display": counter,
                "owner": m.from_user.id,
                "editors": [m.from_user.id],
                "triggers": [],
                "value": 0,
                "step": 1,
            },
        ):
            await m.reply(m.lang.COUNTER_COULDNT_CREATE)
        else:
            await m.reply(m.lang.COUNTER_CREATED)

    async def rem(self, m, counter):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id != data["owner"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_THE_OWNER)
        else:
            os.remove(f"{self.base_dir}{m.chat.id}/{counter}")
            group = self.groups.get(m.chat.id)
            if group and group.get(counter):
                del group[counter]
            await m.reply(
                m.lang.COUNTER_DELETED.format(html.escape(data["display"]), data["value"])
            )

    async def set(self, m, counter, value=None, add=False):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id not in data["editors"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_AN_EDITOR)
        else:
            if add:
                data["value"] += value if isinstance(value, int) else data["step"]
            elif isinstance(value, int):
                data["value"] = value
            self.save(m.chat.id, counter, data)
            self.update_group(m.chat.id, counter, data)
            await m.reply(
                m.lang.COUNTER_SET.format(html.escape(data["display"]), data["value"])
            )

    async def ren(self, m, counter, newname):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id != data["owner"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_THE_OWNER)
        else:
            path = f"{self.base_dir}{m.chat.id}/"
            os.rename(f"{path}{counter}", f"{path}{newname}")
            group = self.groups.get(m.chat.id)
            if group and group.get(counter):
                group[newname] = group[counter]
                del group[counter]["value"]
            await m.reply(m.lang.COUNTER_RENAMED_FROM.format(counter, newname))

    async def display(self, m, counter, display):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id != data["owner"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_THE_OWNER)
        else:
            data["display"] = display
            self.update_group(m.chat.id, counter, data)
            await m.reply(
                m.lang.COUNTER_DISPLAY_SET.format(counter, html.escape(display))
            )

    async def auto_add(self, m, counter, word):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id not in data["editors"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_AN_EDITOR)
        else:
            word = word.lower()
            data["triggers"] += [word]
            self.save(m.chat.id, counter, data)
            group = self.groups.get(m.chat.id)
            if not group:
                group = self.groups[m.chat.id] = {}
            group[counter] = data
            await m.reply(
                m.lang.COUNTER_AUTO_HAS.format(
                    html.escape(data["display"]),
                    html.escape(
                        ", ".join(data["triggers"]),
                    ) or m.lang.COUNTER_NO_TRIGGERS,
                )
            )

    async def auto_del(self, m, counter, word):
        data = self.load(m.chat.id, counter)
        if not data:
            await m.reply(m.lang.COUNTER_DOESNT_EXIST.format(counter))
        elif not m.from_user or m.from_user.id not in data["editors"]:
            await m.reply(m.lang.COUNTER_YOU_ARENT_AN_EDITOR)
        else:
            try:
                data["triggers"].remove(word)
            except Exception:
                await m.reply(
                    m.lang.COUNTER_WORD_NOT_FOUND.format(
                        word,
                        html.escape(
                            ", ".join(data["triggers"]),
                        ) or m.lang.COUNTER_NO_TRIGGERS,
                    )
                )
                return
            self.save(m.chat.id, counter, data)
            if len(data["triggers"]) == 0:
                del self.groups[m.chat.id][counter]
            else:
                self.update_group(m.chat.id, counter, data)
            await m.reply(
                m.lang.COUNTER_AUTO_HAS.format(
                    html.escape(data["display"]),
                    html.escape(
                        ", ".join(data["triggers"]),
                    ) or m.lang.COUNTER_NO_TRIGGERS,
                )
            )

    async def run(self, bot, m):
        async with self.lock:
            args = (m.text or m.caption).split(" ")
            if len(args) > 1:
                if args[1] in ("h", "help"):
                    await m.reply(m.lang.COUNTER_HELP)
                elif args[1] in ("get", "print"):
                    if len(args) <= 2:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    await self.get(m, args[2])
                elif args[1] in ("new", "create"):
                    if len(args) <= 2:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    elif len(args) > 3:
                        await m.reply(m.lang.UNNEEDED_ARGUMENT)
                        return
                    await self.new(m, args[2])
                elif args[1] in ("del", "delete", "remove"):
                    if len(args) <= 2:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    for arg in args[2:]:
                        await self.rem(m, arg)
                elif args[1] in ("ren", "rename"):
                    if len(args) <= 3:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    await self.ren(m, args[2], args[3])
                elif args[1] in ("display", "setdisplay"):
                    if len(args) <= 3:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    await self.display(m, args[2], " ".join(args[3:]))
                elif args[1] in ("add",):
                    if len(args) <= 2:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    try:
                        await self.set(
                            m,
                            args[2],
                            int(args[3]) if len(args) > 3 else None,
                            add=True,
                        )
                    except ValueError:
                        await m.reply(m.lang.COUNTER_ONLY_NUMBERS)
                elif args[1] in ("set",):
                    if len(args) <= 2:
                        await m.reply(m.lang.COUNTER_PROVIDE_NAME)
                        return
                    try:
                        await self.set(m, args[2], int(args[3]) if len(args) > 3 else None)
                    except ValueError:
                        await m.reply(m.lang.COUNTER_ONLY_NUMBERS)
                elif args[1] in ("auto",):
                    if len(args) <= 4:
                        await m.reply(m.lang.INVALID_SYNTAX)
                        return
                    if args[2] in ("add",):
                        await self.auto_add(m, args[3], " ".join(args[4:]))
                    elif args[2] in ("del", "delete", "remove"):
                        await self.auto_del(m, args[3], " ".join(args[4:]))
                else:
                    await m.reply(m.lang.INVALID_SYNTAX)
            else:
                await m.reply(m.lang.COUNTER_HELP)
