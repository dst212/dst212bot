# TODO list of *dst212bot*

- [x] create class Command and base all the commands on that

- [x] buttons on `/help`

- [x] set log chat (boot, shutdown, error reports)

- [x] Remove these files:
  
  - [x] block.py (merge with config.py)

- [x] `command()` on `admin` to improve (detect users)

- [x] create `handlers.py` and put the `inlinequery` in there too, move `commands_map` to commands module's `__init__.py`

- [x] add/remove replied user in `/admin`

- [x] `/info` about groups and channels, detecting the id. if sending `/info` in a group, get info about that group

- [ ] `/pogo`
  
  - [x] add support for both dot `.` and slash `/` as separators for stats
  
  - [ ] ~~help with buttons~~
  
  - [ ] `/pogo` lets you choose data with buttons
  
  - [x] unify `rank` and `iv` and update help
  
  - [ ] pokedex: rename all of the Deoxys without "Forme" in their name

- [x] block unallowed users in `handle_callback`

- [ ] `/pokemon`
  
  - [ ] full search
  
  - [ ] turn é into e and lowerize input (category)
  
  - [ ] fix log not loaded as module

- [ ] `/settings` to add to BotFather

- [ ] per-user settings
  
  - [x] User class
  
  - [x] `/settings` command
    
    - [ ] callback handler

- [ ] support for multiple languages
  
  - [ ] ~~pass message to each `function()` (so as to retrieve settings and change language basing on that)~~
  
  - [x] **IMPORTANT**: the lang will be passed to the `inline()` function and to the `run()` function and shared among the classes' methods as parameter (ugly as fuck but I don't know what else to do)
  
  - [ ] "auto" should rely on `User.language_code` or "en"
  
  - [ ] warn directly log chats on `Users.lang()` if a string is missing
  
  - [ ] adding missing strings:
    
    - [ ] info.py
    
    - [ ] encode.py
    
    - [ ] score.py
  
  - [ ] turn all commands into classes (is it necessary?)
    
    - [x] pokemon/ (results will probably be displayed in English, I don't care)
    
    - [x] pogo/
    
    - [x] random.py
    
    - [x] score.py
    
    - [x] tts.py
    
    - [x] wordfor.py
    
    - [x] translate.py (it is necessary)
      
      - [ ] sync with settings

- [ ] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [ ] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `self.usr`)
  
  - [x] enable media forward from admin's chats (done by using `copy_message()`)
  
  - [x] set support chat
  
  - [x] warn other support chats who replied

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on)
  
  - [ ] `.send chat_id message` command

- [x] ~~***Next giga step***, make commands instances temporary: each command executed is an instance~~ (probably the worst idea I have ever had)

- [x] ~~***Next giga step***, using Rust instead of Python~~ (no, the snek is just ok)
