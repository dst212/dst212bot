# TODO list of *dst212bot*

- [ ] `/pogo`
  
  - [ ] ~~`/pogo` lets you choose data with buttons~~
  
  - [ ] pokedex:
    
    - [ ] duplicate regional forms (e.g. so that "alolan ninetales" and "ninetales alola" give the same result)

- [x] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [x] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `self.usr`)

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on, only admin/support/log chats)
  
  - [ ] make `spam` work when there's a lot of chats (catching FloodWait exception)

- [ ] new command: `/timezone`

- [ ] `/wordfor` add buttons to browse previous and following definitions

- [ ] `/games`? Maybe some stuff like Snake, 2048, Atari Breakout and Tetris

- [ ] add examples (link to GIF on a channel to show how to use some commands)

# Known bugs

- [ ] `/pogo`
  
  - [ ] `ultra friend` not recognized as keyword (due to the ultra league)

- [ ] `/help &amp;` and similar uses of `&` don't get escaped
