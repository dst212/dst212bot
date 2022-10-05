# TODO list of *dst212bot*

- [ ] `/pogo`
  
  - [ ] ~~`/pogo` lets you choose data with buttons~~
  
  - [ ] pokedex:
    
    - [ ] duplicate regional forms (e.g. so that "alolan ninetales" and "ninetales alola" give the same result)
  
- [ ] `/settings`
  
  - [x] add `auto-translate` option
    
    - [ ] make it possible to choose destination language
  
  - [ ] add `set` subcommand

- [ ] support for multiple languages
  
  - [ ] adding missing strings:
    
    - [ ] encode.py
    
    - [ ] score.py

- [ ] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [ ] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `self.usr`)

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on, only admin/support/log chats)
  
  - [ ] `.send chat_id message` command

- [ ] new command: `/timezone`

- [x] `/msgi` sends a json file if the text is too large

- [ ] `/wordfor` add buttons to browse previous and following definitions

- [ ] `/games`? Maybe some stuff like Snake, 2048, Atari Breakout and Tetris

- [ ] add examples (link to GIF on a channel to show how to use some commands)

# Known bugs

- [ ] `/pogo`
  
  - [ ] `ultra friend` not recognized as keyword (due to the ultra league)

- [ ] `/help &amp;` and similar uses of `&` don't get escaped
