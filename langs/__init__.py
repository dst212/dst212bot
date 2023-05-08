import glob
import importlib
import os


def closure():
    langs = {
        lang: importlib.import_module("." + lang, os.path.basename(__path__[0]))
        for lang in [
            os.path.basename(i)[:-3]
            for i in glob.glob(os.path.join(os.path.dirname(__file__), "[!_]*.py"))
            if os.path.isfile(i)
        ]
    }

    def available():
        return [k for k in langs]

    # return the lang dictionary, using English as fallback
    def get(lang):
        return langs[lang].strings if langs.get(lang) else langs["en"].strings

    def formal_name(lang):
        return (
            langs[lang].name or lang
            if langs.get(lang)
            else lang
            if lang == "auto"
            else ""
        )

    def flag(lang):
        return langs[lang].flag if langs.get(lang) else "🏳️"

    class Lang:
        def __init__(self, lang, cfg):
            self.lang = lang
            self.cfg = cfg

        def string(self, s):  # get a specific string of the current language
            text = get(self.lang).get(s) or get("auto").get(s)
            if text is None:
                self.cfg.log(f"A missing string was found: <code>{s}</code>")
                return f"[Missing: <code>{s}</code>]"
            return text

    return Lang, get, formal_name, available, flag


Lang, get, formal_name, available, flag = closure()
del closure
