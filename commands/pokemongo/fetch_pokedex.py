#!/bin/env python3
import json, logging, requests
log = logging.getLogger(__name__)

from bs4 import BeautifulSoup as bs

def main(filename="pokedex.json"):
	links = ("https://pokemondb.net/go/pokedex", "https://pokemondb.net/go/unavailable")
	pokedex = {}
	i = 0
	for link in links:
		log.info(f"Fetching {link}...")
		res = requests.get(link)
		log.info("Parsing...")
		table = bs(res.content, "html.parser").find(id="pokedex").find("tbody")
		log.info("Extracting...")
		for tr in table.find_all("tr"):
			td = tr.find_all("td")
			if len(td) > 0:
				keep = False
				muted = td[1].select_one("small.text-muted") 
				if muted:
					muted = muted.get_text().strip()
					if "Forme" in muted:
						# exclude " Forme" which is six characters long
						muted = td[1].get_text().strip()[:-6]
						keep = True
					else:
						for form in ("Alolan", "Galarian", "Hisuian"):
							if form in muted:
								keep = True
				mon = {
					"id":		int(td[0].select_one("span:nth-of-type(2)").get_text()),
					"name":		muted if keep else td[1].get_text().strip(),
					"attack":	int(td[3].get_text()),
					"defense":	int(td[4].get_text()),
					"hp":		int(td[5].get_text()),
				}
			pokedex[mon["name"].lower()] = mon
			log.debug(mon)
			i += 1
	log.info(f"Fetched data for {i} Pokémons, saving to {filename}...")
	with open(filename, "w") as f:
		json.dump(pokedex, f, separators=(",",":"))
	return pokedex

if __name__ == "__main__":
	main()
