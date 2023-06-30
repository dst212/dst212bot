from custom.misc import format_user
from bot.classes import CustomChat, ChatEncoder

import datetime
import json
import logging
import os
import psutil

from pyrogram.types import User, Message
from pyrogram.raw.functions.messages import ForwardMessages

log = logging.getLogger(__name__)


class Config:
    def __init__(self, bot, users):
        self._me = None
        self._p = psutil.Process()
        self.bot = bot
        self.usr = users
        self.file = "data/config.json"
        self.default = {
            "admin": [],    # can do admin stuff except adding or removing other admins
            "log": [],      # will get info about the bot operations (boot up, shutdown, errors)
            "support": [],  # can see /hey reports
            "helper": [],   # can reply to /hey reports (also admin can do that whether they're helper or not)
            "blocked": [],  # users/chats which can't use the bot
        }
        self.cfg = self.default.copy()
        self.reload()

    # properties
    @property
    def me(self) -> User:
        if not self._me:
            self._me = self.bot.get_users("me")
        return self._me

    @property
    def p(self) -> psutil.Process:
        return self._p

    # methods
    def reload(self) -> None:
        if os.path.exists(self.file):
            obj = {}
            try:
                with open(self.file, "r") as f:
                    obj = json.load(f)
            except Exception as e:
                log.error(e)
                os.rename(
                    self.file,
                    self.file
                    + "."
                    + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    + ".corrupted",
                )
                log.error(f"Couldn't correctly read and parse {self.file}, renamed.")
            # add loaded groups to current config
            for k, v in obj.items():
                self.cfg[k] = [CustomChat(i) for i in v]
        else:
            with open(self.file, "w") as f:
                json.dump(self.cfg, f, indent=2, cls=ChatEncoder)
        if len(self.cfg["admin"]) == 0:
            log.warning(
                f"No admins listed in {self.file}, add one or more. "
                "See https://github.com/dst212/dst212bot/blob/main/README.md#configuration for further details."
            )

    def get(self, what) -> list:
        return self.cfg.get(what) or []

    def get_admins(self) -> list:
        return self.cfg["admin"]

    def get_log_chats(self) -> list:
        return self.cfg["log"]

    def get_support_chats(self) -> list:
        return self.cfg["support"]

    def get_helpers(self) -> list:
        return self.cfg["helper"]

    def get_blocked(self) -> list:
        return self.cfg["blocked"]

    def is_in(self, who, where) -> bool:
        if type(who) != int:
            if type(who) == Message:
                if not who.from_user:
                    return False
                who = who.from_user.id
            elif type(who) == User:
                who = who.id
            else:
                return False
        if type(where) == str:
            return who in self.cfg.get(where)
        for group in where:
            if who in self.cfg.get(group):
                return True
        return False
        # else: True in (who in self.cfg.get(i) for i in where)

    def is_admin(self, who) -> bool:
        return self.is_in(who, "admin")

    def is_helper(self, who) -> bool:
        return self.is_in(who, ["admin", "helper"])

    def is_blocked(self, who) -> bool:
        return self.is_in(who, "blocked")

    def get_users_groups(self, items) -> list:
        out = []
        for i in items:
            try:
                out += [self.bot.get_users(i)]
            except Exception:
                try:
                    out += [self.bot.get_chat(i)]
                except Exception:
                    pass
        return out

    def list_all(self, items) -> str:
        out = []
        for i in items:
            res = None
            try:
                res = self.bot.get_users(i)
            except Exception:
                try:
                    res = self.bot.get_chat(i)
                except Exception:
                    pass
            out += [format_user(res) if res else f"[<code>{i}</code>] (dead)"]
        return ", ".join(out)

    def add_items(self, LANG, group, ids) -> str:
        if group not in self.cfg or group == "admin":
            return LANG("CONFIG_IS_NOT_A_VALID_GROUP").format(group)
        out = ""
        for item in self.get_users_groups(ids):
            if item.id in self.cfg[group]:
                out = LANG("CONFIG_ALREADY_IN").format(format_user(item), group) + "\n"
            else:
                self.cfg[group] += [item.id]
                out = LANG("CONFIG_ADDED_TO").format(format_user(item), group) + "\n"
        with open(self.file, "w") as f:
            json.dump(self.cfg, f, indent=2)
            out = (out or LANG("NOTHING_CHANGED")) + "\n" + LANG("CONFIG_UPDATED")
        return out

    def rem_items(self, LANG, group, ids) -> str:
        if group not in self.cfg or group == "admin":
            return LANG("CONFIG_IS_NOT_A_VALID_GROUP").format(group)
        out = ""
        for item in self.get_users_groups(ids):
            if item.id in self.cfg[group]:
                self.cfg[group].remove(item.id)
                out = (
                    LANG("CONFIG_REMOVED_FROM").format(format_user(item), group) + "\n"
                )
            else:
                out = LANG("CONFIG_NOT_IN").format(format_user(item), group) + "\n"
        with open(self.file, "w") as f:
            json.dump(self.cfg, f, indent=2)
            out = (out or LANG("NOTHING_CHANGED")) + "\n" + LANG("CONFIG_UPDATED")
        return out

    def send_to(
        self,
        targets: list[int],
        text: str,
        forward: list[Message] = [],
        exclude: list[int] = [],
    ):
        for a in targets:
            if a not in exclude:
                try:
                    self.bot.send_message(a.id, text, reply_to_message_id=a.first)
                    for m in forward:
                        self.bot.invoke(ForwardMessages(
                            from_peer=self.bot.resolve_peer(m.chat.id),
                            id=[m.id],
                            random_id=[self.bot.rnd_id()],
                            to_peer=self.bot.resolve_peer(a.id),
                            top_msg_id=a.first,
                        ))
                        # m.copy(a.id, reply_to_message_id=a.first)
                except Exception as e:
                    log.error(f"[{a}] {e}")

    def log(self, text: str, forward: list[Message] = [], exclude: list[int] = []):
        self.send_to(self.get_log_chats(), text, forward, exclude)

    def forward(self, text: str, forward: list[Message] = [], exclude: list[int] = []):
        self.send_to(self.get_support_chats(), text, forward, exclude)
