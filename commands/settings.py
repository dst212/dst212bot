from bot.classes import BaseCommand
from misc.fun import is_admin, can_delete

import html

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified


class CmdSettings(BaseCommand):
    name = "settings"

    def opt2str(self, option_name: str):
        return option_name.upper().replace("-", "_")

    async def button(self, lang, m, callback: str, option_name: str):
        option = await self.usr.get(m.chat, option_name)
        return InlineKeyboardButton(
            f"{lang.string(f"SETTINGS_{self.opt2str(option_name)}")}:"
            f" {("✅" if option else "❌") if type(option) is bool else option}",
            f"{callback} {option_name}",
        )

    async def list_buttons(
        self,
        lang,
        m,
        callback: str,
        option: object,
        start: int = 0,
        step: int = 5,
        back_button: str = None,
        current_value=None,
    ):
        last_page = len(option.options) - ((len(option.options) - 1) % step + 1)
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"⬅️ {lang.BACK}", back_button or self.name)]]
            + [[  # first_row + [[
                InlineKeyboardButton(
                    f"{"✅ " if i == current_value else ""}{option.options.get(i)}",
                    f"{callback} set {i}",
                )
            ] for i in list(option.options.keys())[start:start+step]]
            + (
                [[
                    InlineKeyboardButton("⏪", f"{callback} page 0"),
                    InlineKeyboardButton(
                        "◀", f"{callback} page {max(start-step, 0)}"
                    ),
                    InlineKeyboardButton(
                        "▶", f"{callback} page {min(start+step, last_page)}"
                    ),
                    InlineKeyboardButton("⏩", f"{callback} page {last_page}"),
                ]]
                if last_page != 0
                else []
            )
        )

    async def gen_markup(self, lang, m):
        callback = self.name
        buttons = [
            [InlineKeyboardButton(f"❌ {lang.CLOSE}", f"{callback} close")],
            [InlineKeyboardButton(
                f"🌐 Language: {lang.flag}{lang.name}", f"{callback} lang")],
        ]
        if m.chat.type == ChatType.PRIVATE:
            buttons.append([await self.button(lang, m, callback, "override")])
        else:
            buttons.append([await self.button(lang, m, callback, "auto-tr")])
            buttons.append([await self.button(lang, m, callback, "tr-commands")])
        return InlineKeyboardMarkup(buttons)

    async def callback(self, bot, c):
        m = c.message
        chat = m.chat
        args = c.data.split(" ")
        item = args[1] if len(args) > 1 else None
        value = args[2] if len(args) > 2 else None
        if await is_admin(c):
            text, markup = None, None
            # show main menu of settings
            if item is None:
                text = c.lang.SETTINGS_FOR_THIS_CHAT
            # delete the settings message
            elif item == "close":
                await m.delete()
            # settings in the start message
            elif item == "welcome" or (item == "start" and value is not None):
                if value == "set":
                    value = args[3] if len(args) > 3 else None
                    if value is not None:
                        await self.usr.set(chat.id, "lang", value)
                        c.lang = await self.usr.lang(c)
                text = self.cmds["start"].welcome_message(c)
                markup = self.cmds["start"].markup(c.lang)
            # set value
            else:
                back_button = f"{args[0]}"
                if item == "start":
                    # here value is None, so there's nothing to do but going back to the welcome message
                    back_button = f"{args[0]} welcome"
                    item = "lang"
                option = self.usr.values.get(item)
                if option:
                    current_value = await self.usr.get(chat, item)
                    if option.type == bool:
                        value = not current_value
                    # set value usually for option with multiple possible values
                    elif value == "set":
                        value = args[3] if len(args) > 3 else None
                    # browse pages of multiple values
                    elif value == "page":
                        value = None
                    # change the option's value
                    if value is not None:
                        await self.usr.set(chat.id, item, value)
                        # "lang" may have been changed
                        if item == "lang":
                            c.lang = await self.usr.lang(c)
                        text = c.lang.SETTINGS_FOR_THIS_CHAT
                    # list available options
                    elif option.options:
                        start = int(args[3]) if len(args) > 3 else 0
                        markup = await self.list_buttons(
                            c.lang,
                            m,
                            " ".join(args[:2]),
                            option,
                            start=start,
                            back_button=back_button,
                            current_value=current_value,
                        )
                        text = c.lang.SETTINGS_SELECT_VALUE.format(item, current_value)
            try:
                if text:
                    await c.edit_message_text(
                        text, reply_markup=markup or await self.gen_markup(c.lang, m))
                elif markup:
                    await c.edit_message_reply_markup(markup)
            except MessageNotModified:
                await c.answer(c.lang.NOTHING_CHANGED)
        else:
            await c.answer(c.lang.MUST_BE_ADMIN, show_alert=True)

    async def run(self, bot, m):
        args = (m.text or m.caption).split(" ")
        if await is_admin(m):
            if len(args) > 1:
                if args[1] == "help":
                    await m.reply(m.lang.SETTINGS_HELP)
                elif args[1] == "get":
                    await m.reply_document(
                        f"{self.usr.base_dir}{m.chat.id}", file_name=f"{m.chat.id}.json")
                elif args[1] == "set":
                    if len(args) > 3:
                        item = args[2]
                        value = args[3]
                        option = self.usr.values.get(item)
                        if option:
                            old_value = await self.usr.get(m.chat, item)
                            if option.type == bool:
                                if value.lower() in ("on", "true", "enable"):
                                    value = True
                                else:
                                    value = False
                            if option.is_valid(value):
                                if await self.usr.set(m.chat.id, item, option.type(value)):
                                    await m.reply(
                                        m.lang.SETTINGS_SET_TO.format(
                                            item,
                                            html.escape(value),
                                            old_value))
                                else:
                                    await m.reply(
                                        m.lang.SETTINGS_COULD_NOT_SET.format(
                                            item,
                                            html.escape(value),
                                            old_value))
                            else:
                                await m.reply(
                                    m.lang.SETTINGS_NOT_VALID_VALUE_FOR.format(
                                        html.escape(value), item))
                        else:
                            await m.reply(
                                m.lang.NOT_RECOGNIZED.format(
                                    f"<code>{html.escape(item)}</code>"))
                    else:
                        await m.reply(
                            f"{m.lang.SYNTAX}:\n"
                            f"<code>/{self.name} set &lt;item&gt; &lt;value&gt;</code>"
                        )
                else:
                    await m.reply(m.lang.INVALID_USAGE)
            else:
                if await can_delete(m):
                    await m.delete()
                await bot.send_message(
                    m.chat.id,
                    m.lang.SETTINGS_FOR_THIS_CHAT,
                    reply_markup=await self.gen_markup(m.lang, m),
                    reply_to_message_id=m.reply_to_message_id,
                )
        else:
            await m.reply(m.lang.MUST_BE_ADMIN)
