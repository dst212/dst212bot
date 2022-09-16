import os, requests, json#, shutil
from custom.log import log

API = "https://pokeapi.co/api/v2/"
BASE_DIR = "data/pokemon/"
API_LIST = BASE_DIR + "api.json"

def api_list() -> dict:
	api = {}
	os.makedirs(BASE_DIR, exist_ok=True)
	if not os.path.exists(API_LIST):
		log.info(f"{API_LIST} doesn't exist.")
		with open(API_LIST, "w") as f:
			api = json.loads(requests.get(API).text)
			json.dump(api, f)
			log.info(f"Saved {API_LIST}.")
	else:
		with open(API_LIST) as f:
			api = json.load(f)
	return api

def get_api(key) -> dict:
	api = {}
	os.makedirs(BASE_DIR + key, exist_ok=True)
	file_path = BASE_DIR + key + "/list.json"
	if not os.path.exists(file_path):
		log.info(f"{file_path} doesn't exist.")
		with open(file_path, "w") as f:
			api = {}
			for item in json.loads(requests.get(API + key + "?limit=9999").text)["results"]:
				api[item["name"]] = item["url"]
			json.dump(api, f)
			log.info(f"Saved {file_path}.")
	else:
		with open(file_path) as f:
			api = json.load(f)
	return api

def get_item(item, category) -> dict:
	ret = None
	os.makedirs(BASE_DIR + category, exist_ok=True)
	file_path = BASE_DIR + category + "/" + item + ".json"
	if os.path.exists(file_path):
		with open(file_path) as f:
			try:
				ret = json.load(f)
			except json.decoder.JSONDecodeError:
				log.info(f"Malformed json: {file_path} - deleting it.")
				os.remove(file_path)
	if not ret:
		log.info(f"{file_path} doesn't exist.")
		with open(file_path, "w") as f:
			ret = {}
			for k, v in json.loads(requests.get(API + category + "/" + item).text).items():
				if k == "names":
					ret[k] = {}
					for i in v: ret[k][i["language"]["name"]] = i["name"]
				elif k == "effect_entries":
					ret[k] = {}
					for i in v: ret[k][i["language"]["name"]] = i["effect"]#.replace("\n", " ")
				elif k == "effect_changes" and k and v:
					ret[k] = {}
					for i in v[0]["effect_entries"]: ret[k][i["language"]["name"]] = i["effect"]#.replace("\n", " ")
				elif k == "flavor_text_entries":
					ret[k] = {}
					for i in v: ret[k][i["language"]["name"]] = i["flavor_text"] if "flavor_text" in i else i["text"] if "text" in i else ""#.replace("\n", " ")
				elif k == "descriptions":
					ret[k] = {}
					for i in v: ret[k][i["language"]["name"]] = i["description"]
				elif k == "learned_by_pokemon":
					ret[k] = {}
					for i in v: ret[k][i["name"]] = i["url"]
				elif k == "moves":
					ret[k] = {}
					for i in v: ret[k][i["move"]["name"]] = {
						"level": i["version_group_details"][-1]["level_learned_at"],
						"method": i["version_group_details"][-1]["move_learn_method"]["name"],
					}
				elif k == "abilities":
					ret[k] = {}
					for i in v: ret[k][i["ability"]["name"]] = {
						"is_hidden": i["is_hidden"],
					}
				elif k == "stats":
					ret[k] = {}
					for i in v: ret[k][i["stat"]["name"]] = {
						"base_stat": i["base_stat"],
						"effort": i["effort"],
					}
				elif k == "types":# or k == "past_types":
					ret[k] = []
					for i in v: ret[k] += [i["type"]["name"]]
				elif k == "past_types":
					pass
				elif k == "game_indices":
					ret[k] = {}
					for i in v: ret[k][(i["version"] if "version" in i else i["generation"])["name"]] = i["game_index"]
				elif k == "held_items":
					ret[k] = {}
					for i in v:
						ret[k][i["item"]["name"]] = {}
						for j in i["version_details"]:
							ret[k][i["item"]["name"]][j["version"]["name"]] = j["rarity"]
				else:
					ret[k] = v
			json.dump(ret, f, indent=4)
			log.info(f"Saved {file_path}.")
	return ret
