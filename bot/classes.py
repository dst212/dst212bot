import logging

from pyrogram import filters

log = logging.getLogger(__name__)


class BaseCommand:
    cache_time = 300
    args = []
    aliases = []
    examples = []
    inline_args = []

    def __init__(self, cmds):
        self.usr = cmds.usr
        self.sudo = cmds.sudo
        self.cmds = cmds.map

    def init(self, bot):
        aliases = f"({self.name}|{"|".join(self.aliases)})" if self.aliases else self.name
        bot.on_message(filters.command([self.name, *self.aliases]))(self.run)
        bot.on_callback_query(filters.regex(rf"^({self.name} |{self.name}$)"))(self.callback)
        bot.on_inline_query(filters.regex(rf"^{aliases} "))(self.inline)

    async def run(self, bot, m):
        await m.reply("@dst212 is pretty stupid and forgot to link the correct function.")
        raise Warning("Yoo dst are you dumb")

    async def callback(self, bot, c):
        log.warning(f"Ignoring callback: {c.data}")
        c.continue_propagation()

    async def inline(self, bot, q):
        log.warning(f"Ignoring query: {q.query}")
        q.continue_propagation()
