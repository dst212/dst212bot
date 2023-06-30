from json import JSONEncoder


class CustomCallbackQuery:
    def __init__(self, callback):
        self.callback = callback  # the object itself
        self.text = callback.data  # the text of the query
        self.args = callback.data.split(" ")  # the arguments splitted


class CustomInlineQuery:
    def __init__(self, inline):
        self.inline = inline  # the object itself
        self.text = inline.query  # the text of the query
        self.args = inline.query.split(" ")  # the arguments splitted


class BaseCommand:
    def __init__(self, data):
        self.usr = data["users"]
        self.cfg = data["config"]
        self.cmds = data["commands"]

        self.cache_time = 300
        # self.name = ""
        self.args = []
        self.aliases = []
        self.examples = []
        self.inline_args = []

    def run(self, LANG, bot, m):
        # LANG = lambda s : self.usr.lang(m, s)
        m.reply("@dst212 is pretty stupid and forgot to link the correct function.")
        raise Warning("Yoo dst are you dumb")

    def callback(self, LANG, bot, c):
        pass

    def inline(self, LANG, bot, q):
        pass


class CustomChat:
    def __init__(self, chat_id, topic=None):
        self._id, self._first = (
            (chat_id[0], chat_id[1]) if type(chat_id) == list
            else (chat_id, topic) if type(chat_id) == int
            else (None, None)
        )

    @property
    def id(self):
        return self._id

    @property
    def first(self):
        return self._first

    def __eq__(self, c):
        return self.id == (
            c if type(c) == int
            else c.id if type(c) == type(self)
            else None
        )

    def default(self):
        return [self.id, self.first] if type(self.first) == int else self.id


class ChatEncoder(JSONEncoder):
    def default(self, o):
        return o.default() if type(o) == CustomChat else o
