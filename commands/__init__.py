#from . import admin, base, counter, encode, hey_admins, info, misc, pickrandom, pokemon, pokemongo, qrcode, rand, score, scramble, settings, translate, tts, wordfor
from glob import glob
import os
from . import pokemon, pokemongo
__all__ = [os.path.basename(i)[:-3] for i in glob(os.path.join(os.path.dirname(__file__), "*.py")) if os.path.isfile(i) and not i.startswith("_")]

from . import *

class Commands:
	def __init__(self, bot, users, config):
		data = {"users": users, "config": config}

		self.admin = admin.CmdAdmin(data)
		self.reboot = admin.CmdReboot(data)

		self.base = base
		self.misc = misc
		self.counter = counter.CmdCounter(data)
		self.encode = encode.CmdEncode(data)
		self.hey_admins = hey_admins.CmdHey(data)
		self.info = info.CmdInfo(data)
		self.pickrandom = pickrandom.CmdPickRandom(data)
		self.pokemon = pokemon.CmdPokemon(data)
		self.pokemongo = pokemongo.CmdPoGo(data)
		self.qrcode = qrcode.CmdQRCode(data)
		self.random = rand.CmdRand(data)
		self.score = score.CmdScore(data)
		self.scramble = scramble.CmdScramble(data)
		self.settings = settings.CmdSettings(data)
		self.translate = translate.CmdTranslate(data)
		self.tts = tts.CmdTTS(data)
		self.wordfor = wordfor.CmdWordFor(data)

		self.map = {
			# base commands
			"start": self.base.CmdStart(data),
			"help": self.base.CmdHelp(data),
			"credits": self.base.CmdCredits(data),

			# misc commands
			"ping": self.misc.CmdPing(data),
			"say": self.misc.CmdSay(data),
			"msgi": self.misc.CmdMsgInfo(data),
			"count": self.misc.CmdCount(data),
			"len": self.misc.CmdLength(data),
			"imdumb": self.misc.CmdImDumb(data),
			"tricyclepenisboat": self.misc.CmdTPB(data),
			"delall": self.misc.CmdPurge(data),

			# specific commands
			"settings": self.settings,
			"hey": self.hey_admins, "feedback": self.hey_admins,
			"info": self.info, "i": self.info,
			"encode": self.encode, "e": self.encode,
			"scramble": self.scramble,
			"random": self.random, "r": self.random,
			"pickrandom": self.pickrandom, "pr": self.pickrandom,
			"pokemon": self.pokemon, "p": self.pokemon,
			"pogo": self.pokemongo,
			"translate": self.translate, "tr": self.translate,
			"tts": self.tts,
			"qr": self.qrcode,
			"wordfor": self.wordfor,

			# monitoring commands
			"score": self.score,
			"counter": self.counter,

			# administration commands
			"reboot": self.reboot,
			"admin": self.admin,
			"sudo": self.admin,
		}