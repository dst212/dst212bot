from . import en#, it

def closure():
	langs = {
		"en": {
			"formal-name": en.name,
			"strings": en.strings,
		},
		# "it": it,
	}
	def available():
		return [k for k in langs]
	def get(lang): # return the lang dictionary
		return langs[lang]["strings"] if langs.get(lang) else langs["en"]["strings"]
	def formal_name(lang):
		return langs[lang].get("formal-name") or "" if langs.get(lang) else ""

	class Lang:
		def __init__(self, lang):
			self.__lang = lang

		def string(self, s): # get a specific string of the current language
			return get(self.__lang).get(s) or get("auto").get(s) or f"[Missing: <code>{s}</code>]"

	return Lang, get, formal_name, available
Lang, get, formal_name, available = closure()
del closure
