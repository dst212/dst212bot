class CallbackQuery:
	def __init__(self, callback):
		self.callback = callback				# the object itself
		self.text = callback.data				# the text of the query
		self.args = callback.data.split(" ")	# the arguments splitted

class InlineQuery:
	def __init__(self, inline):
		self.inline = inline 				# the object itself
		self.text = inline.query			# the text of the query
		self.args = inline.query.split(" ")	# the arguments splitted

class Command:
	def __init__(self, data):
		self.usr = data["users"]
		self.cfg = data["config"]
		self.cmds = data["commands"]

		self.cache_time = 300
		# self.name = ""
		self.args = []
		self.aliases = []
		self.examples = []
		self.inline_args = []

	def run(self, LANG, bot, m):
		# LANG = lambda s : self.usr.lang(m, s)
		m.reply("@dst212 is pretty stupid and forgot to link the correct function.")
		raise Warning("Yoo dst are you dumb")

	def callback(self, LANG, bot, c):
		pass

	def inline(self, LANG, bot, q):
		pass
