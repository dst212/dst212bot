class Query:
	def __init__(self, inline):
		self.inline = inline 				# the object itself
		self.text = inline.query			# the text of the query
		self.args = inline.query.split(" ")	# the arguments splitted

class Command:
	def __init__(self, data):
		self.usr = data["users"]
		self.cfg = data["config"]
		self.cache_time = 300

	def run(self, LANG, bot, m):
		# LANG = lambda s : self.usr.lang(m, s)
		m.reply("@dst212 is pretty stupid and forgot to link the correct function.")
		raise Warning("Yoo dst are you dumb")

	def inline(self, LANG, bot, q):
		pass
