import random

def function(args: list) -> int:
	min_num = 0
	max_num = 100
	try: min_num = int(args[1])
	except: pass
	try: max_num = int(args[2])
	except: max_num += min_num
	if min_num > max_num:
		min_num, max_num = max_num, min_num
	elif min_num == max_num:
		max_num += 1
	return random.randrange(min_num, max_num)

def command(LANG, bot, message):
	message.reply_text(function((message.text or message.caption).split(" ")))
