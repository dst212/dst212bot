import logging, os, glob, importlib
log = logging.getLogger(__name__)
from bot.classes import Command

class Commands:
	def __init__(self, bot, users, config):
		self.map = {}
		data = {"users": users, "config": config, "commands": self.map}

		log.info("Loading commands' classes...")
		# import all files/dirs in this path and instance their Command classes in a dictionary
		for i in glob.glob(os.path.join(__path__[0], "[!_]*")):
			if os.path.isfile(i) and i.endswith(".py"):
				i = os.path.basename(i[:-3])
			elif os.path.isdir(i):
				i = os.path.basename(i)
			else:
				continue
			for cmd in [v for _, v in importlib.import_module("." + i, os.path.basename(__path__[0])).__dict__.items() if v != Command and isinstance(v, type) and issubclass(v, Command)]:
				inst = cmd(data)
				if self.map.get(inst.name):
					log.warning(f"Found duplicate command name: {inst.name} of {cmd}, skipping this")
				else:
					self.map[inst.name] = inst
					for alias in inst.aliases:
						self.map[alias] = inst
		log.info(f"Loaded {len(self.map)} commands (aliases included)")
