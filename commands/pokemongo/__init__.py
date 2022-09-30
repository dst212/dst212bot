from bot.classes import Command
from . import rank
from .fetch_pokedex import main as fetch_pokedex
import re, os, json, threading
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

class CmdPoGo(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "pogo"
		self.args = ["arguments"]
		self.inline_args = ["arguments"]

		self.base_dir = f"./data/cache/{self.name}/"
		self.pokedex_file = f"{self.base_dir}pokedex.json"
		self.pokedex = {}

		threading.Thread(target=self.load_pokedex).start()

	def load_pokedex(self) -> dict:
		self.pokedex = {}
		if os.path.exists(self.pokedex_file):
			with open(self.pokedex_file, "r") as f:
				self.pokedex = json.load(f)
		else:
			self.pokedex = fetch_pokedex(self.pokedex_file)

	#buttons below the message to see other ranks
	def rank_buttons(self, rank, min_iv):
		max_rank = pow(16-min_iv, 3)
		l = [rank - 10, rank - 1, rank + 1, rank + 10]
		i = 0
		while i < len(l):
			if l[i] < 1:
				l[i] += max_rank
			elif l[i] > max_rank:
				l[i] %= max_rank
			i += 1
		return l

	def markup(self, c, original=None):
		if c:
			if original is None:
				original = c[1]
			callback = f"{self.name} {c[0]}" + " {} " + " ".join([str(i) for i in c[2:]])
			r = self.rank_buttons(c[1], c[3])
			return InlineKeyboardMarkup([
				[InlineKeyboardButton(f"🔼 #{original}", callback.format(original))],
				[
					InlineKeyboardButton(f"◀ #{r[1]}", callback.format(r[1])),
					InlineKeyboardButton(f"#{r[2]} ▶", callback.format(r[2])),
				],
				[
					InlineKeyboardButton(f"⏪ #{r[0]}", callback.format(r[0])),
					InlineKeyboardButton(f"#{r[3]} ⏩", callback.format(r[3])),
				],
			])
		return None

	def function(self, LANG, args: list[str]):
		title, out, config = None, None, None
		if len(args) > 1:
			if args[1] in ("h", "help"):
				out = LANG('POGO_HELP')
			else:
				title, out, config = rank.get_rank(self, LANG, args[1:])
		else:
			out = LANG('POGO_HELP')
		return title, out or LANG('POGO_INVALID_USAGE'), config

	def run(self, LANG, bot, m):
		msg = m.reply_text(LANG('LOADING'))
		args = (m.text or m.caption).split(" ")
		title, out, config = self.function(LANG, args)
		msg.edit_text(f"<b>{title}</b>\n\n" + out if title else out, reply_markup=self.markup(config))

	def inline(self, LANG, bot, q):
		title, out, config = self.function(LANG, q.args)
		return [InlineQueryResultArticle(
			title = title or "Pokémon GO",
			input_message_content = InputTextMessageContent(f"<b>{title}</b>\n\n{out}"),
			description = re.sub("<[a-z/]*>","", out),
			reply_markup = self.markup(config)
		)]

	def callback(self, LANG, bot, c):
		# c.callback.edit_message_text(LANG('LOADING'))
		title, out, config = self.function(LANG, c.args)
		original = c.callback.message.reply_markup.inline_keyboard[0][0].callback_data.split(" ")[-4]
		try:
			c.callback.edit_message_text(f"<b>{title}</b>\n\n" + out if title else out, reply_markup=self.markup(config, original))
		except MessageNotModified as e:
			c.callback.answer(LANG('POGO_THAT_IS_THE_ONE_THERE'))
