import random

class PickRandom:
	def __init__(self, users):
		self.__usr = users

	def function(self, items: list, limit=1):
		out = ""
		if limit > len(items):
			limit = len(items)
		for i in range(limit):
			out += items.pop(random.randrange(0, len(items))) + "\n"
		return out

	def command(self, LANG, bot, message):
		if not message.reply_to_message:
			message.reply_text(LANG('PICK_RANDOM_REPLY_TO_A_MESSAGE'))
		else:
			args = (message.text or message.caption).split(" ")
			out = ""
			limit = 1
			if len(args) > 1:
				try:
					limit = int(args[1])
				except:
					out = LANG('IS_INVALID_USING').format(args[1], 1)
			out += self.function((message.reply_to_message.text or message.reply_to_message.caption).split("\n"), limit)
			message.reply_text(out)