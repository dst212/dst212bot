# dst212bot

Try this bot out at [dst212bot.t.me](https://dst212bot.t.me).
Updates at [dst212botnews.t.me](https://dst212botnews.t.me).

Note that this is just a random project which offers commands I often need when I'm using Telegram. Also, I don't like the snek, but `pyrogram` is cool.

## Relevant commands

- `help` - get further info about command usage
- `start` - get a warm welcome
- `settings` - customize bot's preferences
- `admin` - manage bot's configuration
- `translate` - translate a message into another language
- `tts` - text to speech
- `qr` - create or read a qr code
- `wordfor` - get a word by an input definition
- `pokemon` - data about Pokémon
- `pogo` - data about Pokémon GO
- `encode` - encode input text from and into binary, base64 or simple text
- `score` - manage the scores created in a chat
- `counter` - manage the counters created in a chat
- `random` - generate a random number
- `pickrandom` - pick a random item from a list
- `scramble` - randomize input text
- `say` - make the bot say something
- `len` - get the length of a message
- `count` - count the messages sent in a chat
- `info` - get info about a chat
- `hey` - contact an admin through the bot
- `credits` - show credits

## Setup

First, install the required python packages (maybe into a [virtual environment](https://docs.python.org/3/tutorial/venv.html)):

```shell
$ python3 -m pip install -r requirements.txt
```

Ensure having a bot token provided by [BotFather](https://botfather.t.me) and an API key (required by `pyrogram`) which can be set at [my.telegram.org](https://my.telegram.org/apps).

Create a file named `variables.py` in the root folder of the repository and put the bot token and the API key in there, so as to make it look like this:

```python
BOTNAME = "dst212bot" # you can put whatever name you want here
TOKEN = "0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
API_ID = "12345678"
API_HASH = "c2306f38edaeb5694c37cdf52b7d573d"
```

To start the bot, just launch the [`main.py`](main.py) script:

```shell
$ chmod +x main.py
$ ./main.py
```

## Configuration

The bot's configuration can be edited while the bot is running through the `/admin` command. The bot won't have any admin the first time it's started, though.

You can add a Telegram user ID (retrievable with `/info`) to the JSON file created at `data/config.json` to make them admin, like this:

```json
{
  "admin":   [448025569, 1390873424],
  "log":     [],
  "helper":  [],
  "support": [],
  "blocked": []
}
```

Then restart the bot (killing it or `CTRL-C`-ing it or whatever you want). Note that admins can restart the bot using the `/reboot` command. This won't work the first time as nobody is an admin unless the configuration file is manually created before.

You may want to edit other things manually:

- `blocked`: blocked chats (users or groups who won't be able to use the bot);

- `helper`: users who can reply to feedback sent with /hey (also users in `admin` can do that);

- `log`: chats logging bot events (when the bot starts or stops, errors... but not /hey feedback);

- `support`: chats receiving feedback sent with /hey.

## Other notes

The script located at [`commands/pokemongo/fetch_pokedex.py`](commands/pokemongo/fetch_pokedex.py) fetches the Pokémon Go pokédex from [pokemondb.net](https://pokemondb.net/go/pokedex) and saves it to `data/cache/pogo/pokedex.json` upon the first start. It can be run manually (this way it creates the file into the running directory).

The [TODO list](TODO.md) is just there to make the project look professional (even though it isn't) and it serves as a common TODO list. You may want to check it out and you may suggest new features too (any constructive criticism is welcome, you can yell at me through any of my contacts available [here](https://dst212.github.io/?page=info#contacts-list)).

## Credits

Used libraries:

- [`pyrogram`](https://pyrogram.org/): Telegram client
- [`opencv-python`](https://pypi.org/project/opencv-python/): QR code detection and decoding
- [`pyqrcode`](https://pypi.org/project/PyQRCode/): QR code generation
- [`googletrans-py`](https://github.com/bllendev/py-googletrans): Translation APIs
- [`gtts`](https://pypi.org/project/gTTS/): Text to speech APIs
- [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/): HTML parser
- [`psutil`](https://pypi.org/project/psutil/): processes info gathering

Data sources:

- Reverse Dictionary: https://reversedictionary.org
- Pokémon: https://pokeapi.co/
- Pokémon GO: https://pokemondb.net/
