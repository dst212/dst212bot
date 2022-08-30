class Query:
	def __init__(self, inline):
		pass
	def inline():
		pass
	def text():
		pass
	def args():
		pass

class Command:
	def __init__(self, users, config):
		self.usr = users
		self.cfg = config

	def run(self, bot, m):
		# LANG = lambda s : self.usr.lang(m, s)
		pass

	def inline(self, bot, query):
		pass
