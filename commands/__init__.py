from bot.classes import BaseCommand
from misc.fun import quick_answer

import glob
import importlib
import logging
import os
import traceback

from pyrogram import filters

log = logging.getLogger(__name__)


class Commands:
    def __init__(self, bot, users, sudo):
        self.map = {}
        self.usr = users
        self.sudo = sudo

        log.info("Loading commands' classes...")
        # Import all files/dirs in this path and instance their Command classes in a dictionary
        for i in glob.glob(os.path.join(__path__[0], "[!_]*")):
            if os.path.isfile(i) and i.endswith(".py"):
                i = os.path.basename(i[:-3])
            elif os.path.isdir(i):
                i = os.path.basename(i)
            else:
                continue
            for Cmd in [
                v
                for _, v in importlib.import_module(
                    f".{i}", os.path.basename(__path__[0])).__dict__.items()
                if v is not BaseCommand and isinstance(v, type) and issubclass(v, BaseCommand)
            ]:
                cmd = Cmd(self)
                if self.map.get(cmd.name):
                    log.warning(
                        f"Found duplicate command name: {cmd.name} of {Cmd}, skipping this.")
                else:
                    cmd.init(bot)
                    self.map[cmd.name] = cmd
                    # for alias in cmd.aliases:
                    #     self.map[alias] = cmd

        @bot.on_message(filters.text, group=-1)
        async def _(bot, m):
            try:
                await self.map["translate"].translate_message(m)
            except Exception:
                traceback.print_exc()
                log.error(f"{m}")
            try:
                await self.map["counter"].parse_message(m)
            except Exception:
                traceback.print_exc()
                log.error(f"{m}")
            m.continue_propagation()

        @bot.on_inline_query(filters.regex(r"^."))
        async def _(bot, q):
            for name, cmd in self.map.items():
                if name.startswith(q.query) and cmd.inline_args:
                    await quick_answer(q, f"{name} {" ".join(cmd.inline_args)}", f"h_{name}")
                    return
            q.continue_propagation()

        @bot.on_inline_query()
        async def _(bot, q):
            await quick_answer(q, q.lang.HELP, "h")

        log.info(f"Loaded {len(self.map)} commands (aliases excluded).")
