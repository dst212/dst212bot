# dst212bot

Try this bot out at [dst212bot.t.me](https://dst212bot.t.me).
Updates at [dst212botchangelog.t.me](https://dst212botchangelog.t.me).

Note that this is just a random project which offers commands I often need when I'm using Telegram. Also, I don't like the snek, but `pyrogram` is cool.

Relevant commands:

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
- `info` - get info about an user
- `hey` - contact an admin through the bot
- `credits` - show credits

The script located at [`commands/pokemongo/fetch-pokedex.py`](commands/pokemongo/fetch-pokedex.py) updates the [`pokedex.json`](commands/pokemongo/pokedex.json) file from [pokemondb.net](https://pokemondb.net/go/pokedex).

The [TODO list](TODO.md) is just there to make the project look professional (even though it isn't) and it serves as a common TODO list. You may want to check it out and you may suggest new features too (any constructive criticism is welcome, you can yell at me through any of my contacts available [here](https://dst212.github.io/?page=info#contacts-list)).

# Credits

Used libraries:

- `pyrogram`: Telegram client
- `opencv-python`: QR code detection and decoding
- `pyqrcode`: QR code generation
- `googletrans` (3.1.0a0): Translation APIs
- `gtts`: Text to speech APIs

Data sources:

- Reverse Dictionary: https://reversedictionary.org
- Pokémon: https://pokeapi.co/
- Pokémon GO: https://pokemondb.net/
