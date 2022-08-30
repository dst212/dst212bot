#!/bin/env python3
from math import floor
import json, re
from custom.find_matches import find_most_accurate

CPM = [0.09399999678, 0.1351374321, 0.1663978696, 0.1926509132, 0.2157324702, 0.2365726514, 0.2557200491, 0.2735303721, 0.2902498841, 0.3060573814, 0.3210875988, 0.335445032, 0.3492126763, 0.3624577366, 0.3752355874, 0.3875924077, 0.3995672762, 0.4111935532, 0.4225000143, 0.4329264205, 0.4431075454, 0.4530599482, 0.4627983868, 0.4723360853, 0.481684953, 0.4908558072, 0.499858439, 0.508701749, 0.5173939466, 0.5259425161, 0.5343543291, 0.5426357538, 0.5507926941, 0.5588305845, 0.5667545199, 0.5745691281, 0.5822789073, 0.5898879079, 0.5974000096, 0.6048236487, 0.6121572852, 0.619404108, 0.6265671253, 0.6336491787, 0.6406529546, 0.6475809714, 0.6544356346, 0.6612192658, 0.6679340005, 0.6745818856, 0.6811649203, 0.6876849013, 0.6941436529, 0.700542901, 0.7068842053, 0.7131690749, 0.7193990946, 0.7255755869, 0.7317000031, 0.7347410386, 0.7377694845, 0.7407855797, 0.7437894344, 0.7467811972, 0.749761045, 0.7527290997, 0.7556855083, 0.7586303702, 0.7615638375, 0.7644860496, 0.7673971653, 0.7702972937, 0.7731865048, 0.7760649471, 0.7789327502, 0.7817900508, 0.7846369743, 0.7874736085, 0.7903000116, 0.792803968, 0.7953000069, 0.7978038984, 0.8003000021, 0.8028038719, 0.8052999973, 0.8078038508, 0.8102999926, 0.8128038352, 0.8152999878, 0.8178038066, 0.820299983, 0.8228037786, 0.8252999783, 0.8278037509, 0.8302999735, 0.8328037534, 0.8353000283, 0.8378037559, 0.8403000236, 0.842803729, 0.8453000188, 0.8478037024, 0.850300014, 0.852803676, 0.8553000093, 0.8578036499, 0.8603000045, 0.862803624, 0.8652999997]
CPM2 = [i**2 for i in CPM]
CPM4 = [i**2 for i in CPM2]

def index(arr: list[float], item: float):
	i = 0
	j = len(arr) - 1
	while(i <= j):
		k = (i + j ) >> 1
		if arr[k] < item:
			i = k + 1
		elif arr[k] > item:
			j = k - 1
		else:
			return k
	return i - 1

def actual_lvl(lvl: float) -> int:
	return int((lvl-1)*2)

def h_lvl(lvl: int) -> float:
	return lvl/2+1

def cp(lvl: float, atk: int, dfn: int, hp: int):
	return floor(max(10, (atk * (dfn * hp)**0.5 * CPM2[lvl]) / 10))

def level(atk: int, dfn: int, hp: int, max_cp: int, max_lvl: float):
	return min(max_lvl, index(CPM4, (max_cp+1)**2 * 100 / (atk**2 * dfn * hp)))

def product(lvl: float, atk: int, dfn: int, hp: int):
	return CPM2[lvl]*atk*dfn*floor(CPM[lvl]*hp)

def get_rank_list(pkm: dict, min_iv: int, max_cp: int, max_lvl: float) -> list[list[int]]:
	products = []
	for a_iv in range(min_iv, 16):
		for d_iv in range(min_iv, 16):
			for h_iv in range(min_iv, 16):
				a = floor(pkm["attack"]) + a_iv
				d = floor(pkm["defense"]) + d_iv
				h = floor(pkm["hp"]) + h_iv
				l = level(a,d,h,max_cp,max_lvl)
				p = product(l,a,d,h)
				products += [[p,
					a_iv,d_iv,h_iv,
					# a,d,h,
					h_lvl(l),
				]]
	products.sort(key=lambda x: x[0],reverse=True)
	return products

def pokemon_output(pkm: dict, v: list, first: int, rank: int, max_cp: int, min_iv: int, max_lvl: int, i: int=-1) -> (str, str):
	title = f'.•°• {pkm["name"]} •°•.'
	out = (
		f'<b>Rank #{rank + 1}</b> ('
	)
	if i != -1 and i != rank:
		out += f'#{i+1} on the list, '
	cpm = CPM[actual_lvl(v[-1])]
	out += (
		f'{round(((16-min_iv)**3-rank)*100000/(16-min_iv)**3)/1000}%)\n' +
		f'<i>Prod</i> : <code>{round(v[0])}</code>, {round(v[0]*100000/first)/1000}%\n\n' +
		f'<i>CP</i> : <code>{cp(actual_lvl(v[-1]), pkm["attack"]+v[1], pkm["defense"]+v[2], pkm["hp"]+v[3])}</code> (cap: <code>{max_cp}</code>)\n' +
		f'<i>Level</i> : <code>{v[-1]}</code> (cap: <code>{max_lvl}</code>)\n' +
		f'<i>IVs</i>: <code>{v[1]}/{v[2]}/{v[3]}</code> (min: <code>{min_iv}</code>)\n\n' +
		'<i>Attack</i> : <code>{}</code>\n'.format(round((pkm["attack"]+v[1])*cpm*100)/100) +
		'<i>Defense</i> : <code>{}</code>\n'.format(round((pkm["defense"]+v[2])*cpm*100)/100) +
		'<i>HP</i> : <code>{}</code>\n'.format(round((pkm["hp"]+v[3])*cpm))
	)
	return title, out

def fix_name(LANG, pkm: str, pokedex: dict) -> (str, str, bool):
	out = ""
	pkm = pkm.lower()
	flag = False
	if pokedex.get(pkm) is None:
		alt = find_most_accurate([k for k,_ in pokedex.items()], pkm)
		if len(alt) == 1:
			pkm = alt[0]
			out += f"{LANG('DID_YOU_MEAN').format(f'<i>{pkm}</i>')}\n\n"
		else:
			if len(alt) > 0:
				out = "Possible matches:\n\n<code>" + "\n".join(alt) + "</code>"
			else:
				out = f"{LANG('NO_RESULTS_FOR').format(f'<i>{pkm}</i>')}\n"
			flag = True
	return out, pkm, flag

def closure():
	pokedex = {}
	with open("commands/pokemongo/pokedex.json", "r") as f:
		pokedex = json.load(f)

	def get_rank(LANG, args: list[str]) -> (str, str):
		title = ""
		# is the pokemon's name more than one word?
		while len(args) > 1 and not re.sub("[\/\.]", "", args[1]).isnumeric():
			args[0] = args[0] + " " + args[1]
			args.pop(1)
		# too few arguments
		if len(args) < 2: return LANG('ERROR'), LANG('POGO_INVALID_USAGE')
		iv = [int(i) for i in re.split("[\/\.]", args[1])]
		# IV are wrong
		if len(iv) != 3 or True in (i < 0 or i > 15 for i in iv):
			return LANG('ERROR'), LANG('POGO_IV_MUST_BE_BETWEEN')
		out, pkm, err = fix_name(LANG, args[0], pokedex)
		# pokemon name not found
		if err: return LANG('NO_RESULTS_FOR').format(f"<i>{pkm}</i>"), out
		pkm = pokedex[pkm]

		try:
			max_cp	= 1500	if len(args) < 3 else int(args[2])
			min_iv	= 0		if len(args) < 4 else int(args[3])
			max_lvl	= 50.0	if len(args) < 5 else float(args[4])
		except ValueError:
			return LANG('ERROR'), LANG('POGO_ENSURE_DATA_IS_CORRECT')
		p = get_rank_list(pkm, min_iv, max_cp, actual_lvl(max_lvl))
		i = 0
		rank = 0
		# search for the pokemon
		for v in p:
			if v[1] == iv[0] and v[2] == iv[1] and v[3] == iv[2]:
				title, tmp = pokemon_output(pkm, v, p[0][0], rank, max_cp, min_iv, max_lvl, i=i)
				out += tmp
				break
			i += 1
			if p[i-1][0] != p[i][0]:
				rank = i
		return title, out

	def get_iv(LANG, args: list[str]) -> (str, str):
		# is the pokemon's name more than one word?
		while len(args) > 1 and not args[1].isnumeric():
			args[0] = args[0] + " " + args[1]
			args.pop(1)
		# too few arguments
		if len(args) < 2: return LANG('ERROR'), LANG('POGO_INVALID_USAGE')
		rank = int(args[1]) - 1
		# IV are wrong
		if not 0 <= rank < 4096:
			return LANG('ERROR'), LANG('POGO_RANK_MUST_BE_INTEGER')
		out, pkm, err = fix_name(LANG, args[0], pokedex)
		# pokemon name not found
		if err: return LANG('NO_RESULTS_FOR').format(f"<i>{pkm}</i>"), out
		pkm = pokedex[pkm]

		try:
			max_cp	= 1500	if len(args) < 3 else int(args[2])
			min_iv	= 0		if len(args) < 4 else int(args[3])
			max_lvl	= 50.0	if len(args) < 5 else float(args[4])
		except ValueError:
			return LANG('ERROR'), LANG('POGO_ENSURE_DATA_IS_CORRECT')

		p = get_rank_list(pkm, min_iv, max_cp, actual_lvl(max_lvl))

		title, tmp = pokemon_output(pkm, p[rank], p[0][0], rank, max_cp, min_iv, max_lvl)
		return title, out + tmp

	return get_rank, get_iv
get_rank, get_iv = closure()
del closure
