from bot.classes import BaseCommand
from custom import command_entry

import html
import logging

from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

log = logging.getLogger(__name__)


# /start
class CmdStart(BaseCommand):
    name = "start"

    def welcome_message(self, m):
        return (
            m.lang.HI_THERE_ADMIN
            if m.from_user.id in self.sudo.admins
            else m.lang.WELCOME_MESSAGE
        ).format(html.escape(m.from_user.first_name))

    def markup(self, lang):
        return InlineKeyboardMarkup([[InlineKeyboardButton(
            f"🌐 Language: {lang.flag}{lang.name}", "settings start")]])

    async def run(self, bot, m):
        if m.chat.type == ChatType.PRIVATE:
            if len(m.command) > 1:
                cmds = [m.command[1][2:]] if m.command[1].startswith("h_") else []
                await (await m.reply(m.lang.LOADING)).edit(
                    **await self.cmds["help"].help_buttons(m.lang, cmds))
            else:
                await m.reply(
                    self.welcome_message(m),
                    reply_markup=self.markup(m.lang),
                )
        else:
            me = await bot.get_users("me")
            await m.reply(
                m.lang.HI_THERE_USER.format(
                    html.escape(m.from_user.first_name if m.from_user else m.sender_chat.title)),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        m.lang.LETS_START, url=f"https://{me.username}.t.me/?start")]]
                ),
            )


# /help
class CmdHelp(BaseCommand):
    name = "help"
    args = ["[command]"]

    async def help_buttons(self, lang, cmds):
        if len(cmds) < 1:
            buttons = []
            row = []
            for k, _ in lang.COMMANDS.items():
                row += [InlineKeyboardButton(k, f"{self.name} {k}")]
                if len(row) > 2:
                    buttons += [row]
                    row = []
            buttons += [row]
            return dict(
                text=f"<b>{lang.HELP}</b>\n\n"
                f"{lang.CHOOSE_A_BUTTON}\n\n"
                f"{lang.INLINE_MODE_NOTICE}",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        cmd = self.cmds.get(cmds[0])
        return dict(
            text=command_entry(lang, cmd, entry=cmds[0]),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"⬅️ {lang.BACK}", f"{self.name} /")]]),
        )

    async def run(self, bot, m):
        await (await m.reply(m.lang.LOADING)).edit(**await self.help_buttons(
            m.lang, (m.text or m.caption).split(" ")[1:]))

    async def callback(self, bot, c):
        args = c.data.split(" ")
        await c.edit_message_text(**await self.help_buttons(
            c.lang, [] if len(args) < 2 or args[1] == "/" else [args[1]]))


# /credits
class CmdCredits(BaseCommand):
    name = "credits"

    async def run(self, bot, m):
        await m.reply(m.lang.CREDITS_MESSAGE)
