from .api import get_item

def print_move(res) -> str:
	text = (
		f"""<b>Name</b>: {res["names"]["en"]}\n""" +
		f"""<b>Type</b>: {res["type"]["name"]}\n""" +
		f"""<b>Category</b>: {res["damage_class"]["name"]}\n""" +
		(f"""<b>Power</b>: {res["power"]}\n""" if res["power"] else "") +
		f"""<b>Accuracy</b>: """ + (f"""{res["accuracy"]}%""" if res["accuracy"] else "can't miss") + f"""\n""" +
		f"""<b>PP</b>: {res["pp"]}\n""" +
		("" if res["priority"] == 0 else "<b>Priority</b>: {0:+}\n".format(res["priority"]))
	)
	# meta data
	if res["meta"]:
		if res["meta"].get("ailment_chance"):
			text += f"""<b>Ailment</b>: {res["meta"]["ailment"]["name"]} ({res["meta"]["ailment_chance"]}%)\n"""
		if res["meta"].get("crit_rate"):
			text += f"""<b>Crit rate</b>: +{res["meta"]["crit_rate"]}\n"""
		if res["meta"].get("drain"):
			text += f"""<b>Enegry drain</b>: {res["meta"]["drain"]}%\n"""
		if res["meta"].get("healing"):
			text += f"""<b>Healing</b>: {res["meta"]["healing"]}%\n"""
		if res["meta"].get("flinch_chance"):
			text += f"""<b>Flinch chance</b>: {res["meta"]["flinch_chance"]}%\n"""
		if res["meta"].get("max_hits"):
			if res["meta"]["max_hits"] == res["meta"]["min_hits"]:
				text += f"""<b>Hits</b>: {res["meta"]["max_hits"]}\n"""
			else:
				text += f"""<b>Hits</b>: {res["meta"]["min_hits"]} to {res["meta"]["max_hits"]}\n"""
		if res["meta"].get("max_turns"):
			if res["meta"]["max_turns"] == res["meta"]["min_turns"]:
				text += f"""<b>Turns</b>: {res["meta"]["max_turns"]}\n"""
			else:
				text += f"""<b>Turns</b>: {res["meta"]["min_turns"]} to {res["meta"]["max_turns"]}\n"""
		if res["meta"].get("stat_chance"):
			text += f"""<b>Stat chance</b>: {res["meta"]["stat_chance"]}\n"""
	# effect
	text += f"""\n<b>Effect</b>:\n"""
	if res["effect_entries"]:
		if res["effect_chance"] is not None:
			text += res["effect_entries"]["en"].replace("$effect_chance", str(res["effect_chance"])) + "\n"
		else:
			text += res["effect_entries"]["en"] + "\n"
	if res["effect_changes"]:
		text += res["effect_changes"]["en"] + "\n"
	if not res["effect_changes"] and not res["effect_entries"]:
		text += "Not provided.\n"
	# description
	if res["flavor_text_entries"]:
		text += f"""\n<b>Description</b>:\n{res["flavor_text_entries"]["en"]}\n"""
	# other languages
	text += "\n<b>Other languages</b>:\n"
	for k, v in res["names"].items():
		text += f"<i>{k}</i>: {v}\n" 
	return text

def print_pokemon(res) -> str:
	text = (
		f"""<b>Name</b>: <a href="{res["sprites"]["other"]["official-artwork"]["front_default"]}">{res["species"]["name"].capitalize()}</a>\n""" +
		f"""<b>Number</b>: {res["id"]}\n""" +
		f"""<b>Height</b>: {res["height"]/10} m\n""" +
		f"""<b>Weight</b>: {res["weight"]/10} kg\n""" +
		f"""<b>Type</b>: {", ".join(w.capitalize() for w in res["types"])}\n""" + 
		f"""<b>Ability</b>: {", ".join(" ".join(w.capitalize() for w in k.split("-")) + (" (hidden)" if v["is_hidden"] else "") for k, v in res["abilities"].items())}\n"""
	)
	text += "<b>Stats</b>:\n"
	for k, v in res["stats"].items():
		text += "- " + k.replace("special-", "Sp. ").capitalize() + ": <code>" + str(v["base_stat"]) + "</code>"
		if v["effort"]:
			text += " <i>(drops " + str(v["effort"]) + ")</i>"
		text += "\n"
	# image = fetch_sprite(res["sprites"]["other"]["official-artwork"]["front_default"], str(res["id"]) + "-official-artwork")
	return text

def print_ability(res) -> str:
	text = f"""<b>Name</b>: {res["names"]["en"]}\n"""
	if res["effect_entries"]:
		text += f"""\n<b>Effect</b>: {res["effect_entries"]["en"]}\n"""
	if res["flavor_text_entries"]:
		text += f"""\n<b>Description</b>: {res["flavor_text_entries"]["en"]}"""
	text += "\n<b>Other languages</b>:\n"
	for k, v in res["names"].items():
		text += f"<i>{k}</i>: {v}\n"
	return text

def print_item(res) -> str:
	item_category = get_item(res["category"]["name"], "item-category")
	attributes = ""
	for i in res["attributes"]:
		r = get_item(i["name"], "item-attribute")
		attributes += r["descriptions"]["en"] + ".\n"
	text = (
		f"""<b>Name</b>: <a href="{res["sprites"]["default"]}">{res["names"]["en"]}</a>\n""" +
		f"""<b>Category</b>: {item_category["names"]["en"]}\n"""
	)
	if res["cost"] > 0:
		text += f"""<b>Cost</b>: {res["cost"]} ₽\n"""
	if attributes:
		text += f"""<b>Attributes</b>:\n{attributes}\n"""
	if res["effect_entries"]:
		text += f"""\n<b>Effect</b>: {res["effect_entries"]["en"]}\n"""
	if res["flavor_text_entries"]:
		text += f"""\n<b>Description</b>: {res["flavor_text_entries"]["en"]}\n"""
	return text

def print_data(LANG, item: str, category: str) -> str:
	text = None
	res = get_item(item, category)
	if category == "move":
		text = print_move(res)
	elif category == "pokemon":
		text = print_pokemon(res)
	elif category == "ability":
		text = print_ability(res)
	elif category == "item":
		text = print_item(res)
	else:
		text = LANG('NOT_AVAILABLE_AT_THIS_TIME')
	return text
