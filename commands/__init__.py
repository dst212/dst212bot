from . import admin, base, counter, encode, hey_admins, info, misc, pickrandom, pokemon, pokemongo, qrcode, rand, score, scramble, settings, translate, tts, wordfor

class Commands:
	def __init__(self, bot, users, config):
		self.admin = admin.Admin(users, config)
		self.base = base.Base(users)
		self.counter = counter.Counter(users)
		self.encode = encode.Encode(users)
		self.hey_admins = hey_admins.Hey(users, config)
		self.info = info.Info(users)
		self.misc = misc.Misc(users)
		self.pickrandom = pickrandom.PickRandom(users)
		self.pokemon = pokemon
		self.pokemongo = pokemongo
		self.qrcode = qrcode.QRCode(users)
		self.random = rand
		self.score = score.Score(users)
		self.scramble = scramble.Scramble(users)
		self.settings = settings.Settings(users)
		self.translate = translate
		self.tts = tts
		self.wordfor = wordfor

		self.map = {
			# base commands
			"start": self.base.start,
			"help": self.base.help_command,
			"credits": self.base.credits_command,

			# misc commands
			"ping": self.misc.pong,
			"say": self.misc.say,
			"msgi": self.misc.message_info,
			"count": self.misc.count_messages,
			"len": self.misc.message_length,
			"tricyclepenisboat": self.misc.tpb,
			"delall": self.misc.purge,
			"raiseerror": self.misc.raise_error,

			# specific commands
			"settings": self.settings.command,
			"hey": self.hey_admins.command, "feedback": self.hey_admins.command,
			"info": self.info.command,
			"encode": self.encode.command, "e": self.encode.command,
			"scramble": self.scramble.command,
			"random": self.random.command, "r": self.random.command,
			"pickrandom": self.pickrandom.command, "pr": self.pickrandom.command,
			"pokemon": self.pokemon.command,
			"pogo": self.pokemongo.command,
			"translate": self.translate.command, "tr": self.translate.command,
			"tts": self.tts.command,
			"qr": self.qrcode.command,
			"wordfor": self.wordfor.command,

			# monitoring commands
			"score": self.score.command,
			"counter": self.counter.command,

			# administration commands
			"reboot": self.admin.reboot,
			"admin": self.admin.command,
			"sudo": self.admin.command,
		}