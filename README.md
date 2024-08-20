# dst212bot

Try this bot out at [dst212bot.t.me](https://dst212bot.t.me).
Updates and other bots at [dst212botnews.t.me](https://dst212botnews.t.me).

Note that this is just a random project which offers commands I often need when I'm using Telegram. Also, I don't like the snek, but `pyrogram` is cool.

## Relevant commands

- `help` - Get further info about command usage.
- `settings` - Customize bot's preferences.
- `translate` - Translate a message into another language.
- `tts` - Text to speech.
- `qr` - Create or read a qr code.
- `wordfor` - Get a word by an input definition.
- `pokemon` - Data about Pokémon.
- `encode` - Encode input text from and into binary, base64 or simple text.
- `score` - Manage the scores created in a chat.
- `counter` - Manage the counters created in a chat.
- `random` - Generate a random number.
- `pickrandom` - Pick a random item from a list.
- `shuffle` - Randomize input text.
- `say` - Make the bot say something.
- `len` - Get the length of a message.
- `imdumb` - Raise your intelligence beyond all boundaries.
- `credits` - Show credits.

Commands inherited from `pyrogram-misc`:

- `id` - Retrieve ID of current chat, message, sender.
- `ping` - Ping the bot.
- `inspect` - Get a JSON format of the quoted message.
- `feedback` - Contact the bot owner.
- `sudo` - Manipulate the bot (admins only).

## Setup

First, clone the repo recursively:

```shell
git clone --recursive https://github.com/dst212/dst212bot
```

Install the required python packages (maybe into a [virtual environment](https://docs.python.org/3/tutorial/venv.html)):

```shell
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

Ensure having a bot token provided by [BotFather](https://botfather.t.me) and an API key (required by `pyrogram`) which can be set at [my.telegram.org](https://my.telegram.org/apps).

Create a file named `keys.py` in the root folder of the repository and put the bot token and the API key in there, so as to make it look like this:

```python
TOKEN = "0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
API_ID = "12345678"
API_HASH = "c2306f38edaeb5694c37cdf52b7d573d"
```

The bot configuration is held in config.py:

```python
BOTNAME = "dst212bot"  # You can put whatever name you want here
ADMINS = [448025569]  # Your Telegram ID here (you can get it with /id, until then you can leave this blank)
LOG_CHAT = -100123456789  # Chat you'd like to receive logs in
SUPPORT_CHAT = ADMINS[0]  # Chat where /feedback will forward messages
```

You can also use topics as log or support chats! Send `/id` on the desired topic and use the "Chat" ID and "Reply to" ID:

```python
...
LOG_CHAT = [-100123456789, 54]  # The first number is a supergroup ID, the second one is the ID of the topic
...
```

To start the bot, just launch the [`main.py`](main.py) script:

```shell
# source env/bin/activate # Ensure you had already done this before
./main.py
```

## Other notes

The [TODO list](TODO.md) is just there to make the project look professional (even though it isn't) and it serves as a common TODO list. You may want to check it out and you may suggest new features too (any constructive criticism is welcome, you can yell at me through any of my contacts available [here](https://dst212.github.io/?page=info#contacts-list)) or directly on Telegram ([@dst212](https://dst212.t.me)) or via `/feedback` through the bot.

## Credits

Used libraries:

- [`pyrogram`](https://pyrogram.org/): Telegram client
- [`opencv-python`](https://pypi.org/project/opencv-python/): QR code detection and decoding
- [`pyqrcode`](https://pypi.org/project/PyQRCode/): QR code generation
- [`googletrans-py`](https://github.com/bllendev/py-googletrans): Translation APIs
- [`gtts`](https://pypi.org/project/gTTS/): Text to speech APIs
- [`psutil`](https://pypi.org/project/psutil/): processes info gathering

Data sources:

- Reverse Dictionary: https://reversedictionary.org
- Pokémon: https://pokeapi.co/
