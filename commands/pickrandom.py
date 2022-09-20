from bot.classes import Command
import random

class CmdPickRandom(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "pickrandom"
		self.args = ["[limit]"]
		self.aliases = ["pr"]

	def function(self, items: list, limit=1):
		out = ""
		if limit > len(items):
			limit = len(items)
		for i in range(limit):
			out += items.pop(random.randrange(0, len(items))) + "\n"
		return out

	def run(self, LANG, bot, m):
		if not m.reply_to_message:
			m.reply_text(LANG('PICK_RANDOM_REPLY_TO_A_MESSAGE'))
		else:
			args = (m.text or m.caption).split(" ")
			out = ""
			limit = 1
			if len(args) > 1:
				try:
					limit = int(args[1])
					if limit < 1:
						raise ValueError("Limit must be greater than 1")
				except:
					out = LANG('IS_INVALID_USING').format(args[1], 1)
			out += self.function((m.reply_to_message.text or m.reply_to_message.caption).split("\n"), limit)
			m.reply_text(out)