from bot.classes import BaseCommand
from custom.misc import format_user, sender_is_admin

import html, logging, requests
log = logging.getLogger(__name__)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

class CmdHey(BaseCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "hey"
		self.aliases = ("support", "forward", "bye")
		self.args = ("[text]",)

	# get message data (chat id, message's id to reply to)
	def get_mdata(self, m) -> list[int]:
		text = m.reply_to_message and (m.reply_to_message.text or m.reply_to_message.caption) or ""
		if not text.startswith("#"):
			return None
		args = text[1:].split("#")
		try:
			# chat_id#message_id
			args[0], args[1] = int(args[0]), int(args[1]) if args[1] else None
		except:
			return None
		return args

	# forward a message to helpers
	def forward(self, m):
		sender = format_user(m.from_user or m.sender_chat)
		group = format_user(m.chat) if m.chat.type != ChatType.PRIVATE else None
		info_msg = f"<code>#{m.chat.id}</code><code>#{m.id}#</code>\n"
		info_msg += f"{group}, {sender}:" if group else f"{sender}:"
		self.cfg.forward(info_msg, forward=[m.reply_to_message or m], exclude=[m.chat.id])

	# detect whether a message:
	# - is a reply from helpers (→True)
	# - should be forwarded (→False)
	# - or neither (do nothing, →False)
	def parse(self, bot, m) -> bool:
		mdata = self.get_mdata(m)
		if (
			mdata and m.from_user and
			self.cfg.is_in(m.chat.id, "support") and self.cfg.is_helper(m)
		):
			bot.copy_message(mdata[0], m.chat.id, m.id, reply_to_message_id=mdata[1])
			for i in self.cfg.get_support_chats():
				if i != m.chat.id:
					try:
						bot.send_message(i, format_user(m.from_user or m.sender_chat or m.chat) + f" in reply to <code>#{mdata[0]}</code><code>#{mdata[1]}#</code>")
						bot.forward_message(i, m.chat.id, m.id)
					except Exception as e:
						log.error(f"[{i}] {e}")
			return True
		elif self.usr.do_forward(m.chat.id):
			self.forward(m)
		return False

	def enable(self, LANG, chat, user) -> str:
		if self.usr.enable_forward(chat.id) and self.usr.do_forward(chat.id):
			self.cfg.forward(f"<code>#{chat.id}</code><code>##</code>\n{format_user(user)}:\nChat forward enabled for {format_user(chat)}.")
			return LANG('CHAT_FORWARD_ENABLED').format(f"/{self.aliases[-1]}")
		return LANG('CHAT_FORWARD_COULD_NOT_ENABLE')

	def disable(self, LANG, chat, user) -> str:
		if self.usr.disable_forward(chat.id) and not self.usr.do_forward(chat.id):
			self.cfg.forward(f"<code>#{chat.id}</code><code>##</code>\n{format_user(user)}:\nChat forward disabled for {format_user(chat)}.")
			return f"{LANG('CHAT_FORWARD_DISABLED')}\n{LANG('CHAT_FORWARD_HELPERS_CAN_SEND').format(self.name)}"
		self.cfg.log(f"Chat forward for {format_user(chat)} couldn't be disabled.")
		return LANG('CHAT_FORWARD_STILL_ENABLED')

	def run(self, LANG, bot, m):
		args = (m.text or m.caption or "").split(" ")
		# # if it's /bye or chat-fwd already enabled, disable it
		if self.usr.do_forward(m.chat.id) or args[0][1:] == self.aliases[-1]:
			# helpers can stop the forward themselves
			mdata = self.get_mdata(m)
			if (
				mdata and m.from_user and
				self.cfg.is_in(m.chat.id, "support") and self.cfg.is_helper(m)
			):
				target = bot.get_chat(mdata[0])
				bot.send_message(target.id, self.disable(LANG, target, m.from_user))
			# admins of chat of course can disable chat forward
			elif sender_is_admin(m):
				if self.usr.do_forward(m.chat.id):
					m.reply_text(self.disable(LANG, m.chat, m.from_user))
				else:
					m.reply_text(LANG('CHAT_FORWARD_NOT_ENABLED'))
			# otherwise regular users have no permissions
			else:
				m.reply_text(LANG('NO_PERMISSIONS'))
		# forward a single message only if some text or a message is provided
		elif len(args) > 1 or m.reply_to_message:
			self.forward(m)
		# ask to enable chat forward only if triggered by an admin
		elif sender_is_admin(m):
			m.reply_text(LANG('ENABLE_CHAT_FORWARD'), reply_markup=InlineKeyboardMarkup([[
				InlineKeyboardButton(LANG('YES'), f"{self.name} forward"),
				InlineKeyboardButton(LANG('NO'), f"{self.name} cancel"),
			]]))

	def callback(self, LANG, bot, c):
		if sender_is_admin(c.callback):
			if c.args[1] == "forward":
				c.callback.edit_message_text(self.enable(LANG, c.callback.message.chat, c.callback.from_user))
			elif c.args[1] == "cancel":
				c.callback.edit_message_text(
					LANG('CHAT_FORWARD_NOT_ENABLED') if not self.usr.do_forward(c.callback.message.chat.id) else
					self.disable(LANG, c.callback.message.chat, c.callback.from_user)
				)
		else:
			c.callback.answer(LANG('NO_PERMISSIONS'))
