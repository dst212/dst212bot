# TODO list of *dst212bot*

- [ ] create class AbstractCommand and base all the commands on that

- [x] buttons on `/help`

- [x] set log chat (boot, shutdown, error reports)

- [x] Remove these files:
  
  - [x] block.py (merge with config.py)

- [x] `command()` on `admin` to improve (detect users)

- [x] create `handlers.py` and put the `inlinequery` in there too, move `commands_map` to commands's `__init__.py`

- [x] add/remove replied user in `/admin`

- [x] `/info` about groups and channels, detecting the id. if sending `/info` in a group, get info about that group

- [x] `/pogo` add support for both dot `.` and slash `/` as separators for stats

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
  
  - [x] **IMPORTANT**: the lang will be passed to the `inlinequery()` function and to the `command()` function and shared among the classes' methods as parameter (ugly as fuck but I don't know what else to do)
  
  - [ ] "auto" should rely on `User.language_code` or "en"
  
  - [ ] warn directly log chats on `Users.lang()` if a string is missing
  
  - [ ] adding missing strings:
    
    - [ ] info.py
    
    - [ ] encode.py
    
    - [ ] score.py
  
  - [ ] turn all commands into classes (is it necessary?)
    
    - [ ] pokemon/ (results will probably be displayed in English, I don't care)
    
    - [ ] pogo/
    
    - [ ] random.py
    
    - [x] score.py
    
    - [ ] tts.py
    
    - [ ] wordfor.py
    
    - [ ] translate.py (it is necessary)
      
      - [ ] sync with settings

- [ ] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [ ] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `__usr`)
  
  - [x] enable media forward from admin's chats (done by using `copy_message()`)
  
  - [x] set support chat
  
  - [x] warn other support chats who replied

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on)
  
  - [ ] `.send chat_id message` command

- [ ] ~~***Next giga step***, make commands instances temporary: each command executed is an instance~~

- [ ] ***Next giga step***, using Rust instead of Python
