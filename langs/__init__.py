from . import en#, it

def closure():
	langs = {
		"en": {
			"formal-name": en.name,
			"strings": en.strings,
			"flag": en.flag,
		},
		# "it": it,
	}
	def available():
		return [k for k in langs]
	def get(lang): # return the lang dictionary
		return langs[lang]["strings"] if langs.get(lang) else langs["en"]["strings"]
	def formal_name(lang):
		return langs[lang].get("formal-name") or lang if langs.get(lang) else lang if lang == "auto" else ""
	def flag(lang):
		return langs[lang]["flag"] if langs.get(lang) else "🏳️"

	class Lang:
		def __init__(self, lang, cfg):
			self.lang = lang
			self.cfg = cfg

		def string(self, s): # get a specific string of the current language
			text = get(self.lang).get(s) or get("auto").get(s)
			if text is None:
				self.cfg.log(f"A missing string was found: <code>{s}</code>")
				return f"[Missing: <code>{s}</code>]"
			return text

	return Lang, get, formal_name, available, flag
Lang, get, formal_name, available, flag = closure()
del closure
