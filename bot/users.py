import langs

import asyncio
import datetime
import googletrans
import json
import logging
import re
import os

from pyrogram.types import Chat, User, Message, CallbackQuery, InlineQuery
from pyrogram.enums import ChatType, ChatAction
import pyrogram.errors as Errors

log = logging.getLogger(__name__)


class Option:
    def __init__(
        self, t: type, default, minimum=None, maximum=None, options: dict = {}
    ):
        self.type = t
        self.default = default
        self.min = minimum
        self.max = maximum
        self.options = options

    def is_valid(self, value):
        try:
            value = self.type(value)
        except Exception:
            return False
        return self.type == bool or (
            value in self.options if self.options else self.min <= value <= self.max
        )


class Users:
    def __init__(self, bot):
        self.base_dir = "./data/users/"
        self.unused_dir = "./data/deactivated/"
        self.bot = bot
        self.chat = {}
        self.lock = asyncio.Lock()
        self.values = {
            "override": Option(bool, False),
            "lang": Option(
                str,
                "auto",
                options={
                    i: f"{langs.flag(i)}{langs.formal_name(i)}"
                    for i in ("auto", *langs.langs.keys())
                },
            ),
            "auto-tr": Option(
                str,
                "off",
                options={
                    k: v
                    for i in [
                        {"off": "OFF", "auto": "AUTO"},
                        {k: f"{k} ({v})" for k, v in googletrans.LANGUAGES.items()},
                    ]
                    for k, v in i.items()
                },
            ),
            "tr-commands": Option(bool, False)
        }
        self.default = {k: v.default for k, v in self.values.items()}

        async def apply_lang(_, u):
            setattr(u, "lang", await self.lang(u))
            u.continue_propagation()
        bot.on_message(group=-1)(apply_lang)
        bot.on_inline_query(group=-1)(apply_lang)
        bot.on_callback_query(group=-1)(apply_lang)

    async def save(self, chat_id: int, config: dict = None):
        async with self.lock:
            os.makedirs(self.base_dir, exist_ok=True)
            with open(f"{self.base_dir}{chat_id}", "w") as f:
                json.dump(config or self.default, f)

    async def load(self, chat_id: int) -> dict:
        async with self.lock:
            try:
                file = f"{self.base_dir}{chat_id}"
                # Check if the user was previously deactivated
                if not os.path.exists(file):
                    unused = f"{self.unused_dir}{chat_id}"
                    if os.path.exists(unused):
                        os.rename(unused, file)
                if os.path.exists(file):
                    with open(file, "r") as f:
                        return json.load(f)
            except json.JSONDecodeError:
                os.rename(
                    file,
                    f"{file}.{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.corrupted",
                )
                log.error(f"Couldn't read {file}, renamed.")
        return None

    async def forget(self, chat_id: int):
        if not isinstance(chat_id, int):
            chat_id = int(chat_id)
        async with self.lock:
            file = f"{self.base_dir}{chat_id}"
            if os.path.exists(file):
                log.info(f"Removing settings for {chat_id}...")
                os.remove(file)
                if self.chat.get(chat_id):
                    log.info(f"Removing {self.chat[chat_id]}...")
                    del self.chat[chat_id]
                log.info(f"Successfully erased settings for {chat_id}.")
                return True
        return False

    # Move settings away from the main folder
    # Settings will be re-activated if the user/chat interacts again with the bot
    async def deactivate(self, chat_id: int):
        if not isinstance(chat_id, int):
            chat_id = int(chat_id)
        async with self.lock:
            os.makedirs(self.unused_dir, exist_ok=True)
            file = f"{self.base_dir}{chat_id}"
            log.info(f"Deactivating settings for {chat_id}...")
            if os.path.exists(file):
                os.rename(file, f"{self.unused_dir}{chat_id}")
                if self.chat.get(chat_id):
                    del self.chat[chat_id]
                log.info(f"Successfully deactivated settings for {chat_id}.")
            else:
                log.info(f"{file} not found.")
            return True
        return False

    async def do_override(self, m: Message) -> bool:
        # It's safe to call directly self.get() here
        # It handles the creation of the user's settings if they don't exist
        return m.from_user and await self.get(m.from_user.id, "override")

    # Retrieve user/group id considering the "override" flag
    async def get_id(self, item: User | Chat | Message | InlineQuery | CallbackQuery) -> (User | Chat):
        if type(item) is Message:
            return item.from_user.id if await self.do_override(item) else item.chat.id
        elif type(item) is CallbackQuery:
            return (
                item.from_user.id
                if await self.do_override(item) or not item.message
                else item.message.chat.id
            )
        elif type(item) is InlineQuery:
            return item.from_user.id
        elif type(item) in (Chat, User):
            return item.id
        elif isinstance(item, str) and re.match(r"^(-|)[0-9]+$", item):
            return int(item)
        elif isinstance(item, int):
            return item
        raise ValueError(f"Invaid type: {type(item)}")

    # Get chat's settings or values
    async def get(self, chat, key: str = None):
        chat_id = await self.get_id(chat)
        if not self.chat.get(chat_id):
            log.info(f"Loading settings for {chat_id}...")
            settings = await self.load(chat_id)
            if not settings:
                log.info(f"{chat_id} not found in files, creating...")
                settings = self.default.copy()
                await self.save(chat_id, settings)
            self.chat[chat_id] = settings
            log.info(f"Loaded settings for {chat_id}: {settings}")
        else:
            settings = self.chat[chat_id]
        # Add the option if it wasn't written yet, then save it
        if key:
            if not self.values.get(key):
                return None
            elif settings.get(key) is None:
                settings[key] = self.values[key].default
                await self.save(chat_id, settings)
        return (settings.get(key) if key else settings) if settings else None

    # Modify chat's settings
    async def set(self, chat, key: str, value: object) -> bool:
        chat_id = await self.get_id(chat)
        i = self.values.get(key)
        if self.chat.get(chat_id) and i:
            if i.is_valid(value):
                self.chat[chat_id][key] = i.type(value)
                await self.save(chat_id, self.chat[chat_id])
                return True
            else:
                raise ValueError(
                    f"Type mismatch: {type(self.chat[chat_id][key])} and {type(value)} ({value})")
        return False

    # The user is valid, didn't stop the bot and wasn't deleted
    async def can_send_to(self, chat_id: int) -> bool:
        if chat_id:
            try:
                await self.bot.send_chat_action(chat_id, ChatAction.TYPING)
                await self.bot.send_chat_action(chat_id, ChatAction.CANCEL)
                return True
            except (Errors.UserIsBlocked, Errors.InputUserDeactivated, Errors.ChatWriteForbidden) as e:
                log.info(f"Deactivating [{chat_id}]: {e}")
                await self.deactivate(chat_id)
            except Errors.UserIdInvalid:
                log.info(f"[{chat_id}] is an invalid id. Forgetting it.")
                await self.forget(chat_id)
            except Errors.PeerIdInvalid:
                log.info(f"[{chat_id}] has never interacted with the bot privately.")
            # except Exception as e:
            #     log.warning(f"[{chat_id}]: {e}")
        return False

    # Retrieve all chats' ids for which settings were saved
    def get_all_chats(self):
        chats = []
        for i in os.listdir(self.basr_dir):
            try:
                chats.append(int(i))
            except Exception:
                pass
        return chats

    # Retrieve active chats list
    async def get_active_chats_list(self):
        return await self.get_active_chats(as_list=True, ids=True)

    # Retrieve active chats grouped by chat type
    async def get_active_chats(self, as_list: bool = False, ids: bool = False):
        chats = [] if as_list else {k.name: {} for k in ChatType}
        add = (
            (lambda chat: chats.append(chat.id if ids else chat))
            if as_list
            else (lambda chat: chats[chat.type.name].update({chat.id: chat}))
        )
        for i in os.listdir(self.base_dir):
            try:
                chat = await self.bot.get_chat(i)
                if type(chat) is not Chat:
                    log.warning(f"Settings for {i} are unused. Deactivating.")
                    await self.deactivate(i)
                elif await self.can_send_to(chat.id):
                    add(chat)
            except (Errors.ChannelInvalid, Errors.ChannelPrivate):
                log.warn(f"Channel {i} is private or invalid. Deactivating it.")
                await self.deactivate(i)
            except Errors.UserIdInvalid:
                log.warn(f"[{i}] is an invalid id. Forgetting it.")
                await self.forget(i)
            except Errors.PeerIdInvalid:
                # log.warn(f"Chat {i} never interacted with the bot.")
                pass
            # except Exception as e:
            #     log.warning(f"[{i}]: {e}")
        if not as_list:
            chats["count"] = sum([len(i) for i in chats.values()])
        return chats

    # Messages and queries can (and should) be passed as chat, they will be parsed later on in get_chat()
    async def lang_code(self, chat: User | Chat) -> str:
        lang = await self.get(chat, "lang")
        # Uses user's language code (provided by pyrogram) if the language is "auto"
        if lang != "auto":
            return lang
        if isinstance(chat, Chat) and chat.type is ChatType.PRIVATE:
            try:
                chat = await self.bot.get_users(chat.id)
            except Exception:
                pass
        if isinstance(chat, User):
            return chat.language_code
        return "en"

    async def lang(self, chat_id):
        return langs.get(await self.get(chat_id, "lang"))
