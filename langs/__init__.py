import glob
import importlib
import os


langs = {
    lang: importlib.import_module(f".{lang}", os.path.basename(__path__[0])).init()
    for lang in [
        os.path.basename(i)[:-3]
        for i in glob.glob(os.path.join(__path__[0], "[!_]*.py"))
        if os.path.isfile(i)
    ]
}


# return the lang dictionary, using English as fallback
def get(lang: str = "en"):
    return langs.get(lang) or langs["en"]


def formal_name(lang: str):
    return (
        langs[lang].name or lang
        if langs.get(lang)
        else lang
        if lang == "auto"
        else ""
    )


def flag(lang: str):
    return langs[lang].flag if langs.get(lang) else "🏳️"


class LangString:
    def __init__(self, string: str):
        self._string = string

    @property
    def string(self):
        return self._string

    def apply(self, lang: str | object):
        if not isinstance(lang, type(get())):
            if type(lang) is not str:
                lang = lang.lang
        if type(lang) is str:
            lang = get(lang)
        return lang.__dict__.get(self._string) or f"{self._string}"
