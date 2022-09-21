# TODO list of *dst212bot*

- [ ] `/pogo`
  
  - [ ] `/pogo` lets you choose data with buttons
  
  - [ ] pokedex:
    
    - [ ] duplicate regional forms (e.g. so that "alolan ninetales" and "ninetales alola" give the same result)
  
  - [ ] add buttons to the output message to browse previous and following ranks
  
  - [x] save ranks in json files (instead of re-computing them every time)

- [ ] `/pokemon`
  
  - [ ] full search
  
  - [ ] turn é into e and lowerize input (category)

- [ ] `/settings`
  
  - [ ] `/settings get` to get the json file containing the user/group's settings
  
  - [ ] actually override settings when `override` is true (and remove override in groups or make it like "ignore users' override" which is quite chaotic evil)
  
  - [ ] add `auto-translate` option

- [ ] support for multiple languages
  
  - [ ] adding missing strings:
    
    - [ ] encode.py
    
    - [ ] score.py
  
  - [ ] `/translate` (sync with settings)

- [ ] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [ ] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `self.usr`)

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on, only admin/support/log chats)
  
  - [ ] `.send chat_id message` command

- [ ] new command: `/timezone`

- [ ] `/msgi` sends a json file if the text is too large

- [ ] `/wordfor` add buttons to browse previous and following definitions
