# TODO list of *dst212bot*

- [ ] `/pogo`
  
  - [x] add support for both dot `.` and slash `/` as separators for stats
  
  - [ ] ~~help with buttons~~
  
  - [ ] `/pogo` lets you choose data with buttons
  
  - [x] unify `rank` and `iv` and update help
  
  - [ ] pokedex:
    
    - [x] rename all of the Deoxys without "Forme" in their name (done also for other mons with "Forme" in their name)
    
    - [ ] duplicate regional forms (e.g. so that "alolan ninetales" and "ninetales alola" give the same result)

- [ ] `/pokemon`
  
  - [ ] full search
  
  - [ ] turn é into e and lowerize input (category)

- [ ] `/settings`
  
  - [ ] per-user settings
  - [ ] callback handler

- [ ] support for multiple languages
  
  - [x] **IMPORTANT**: the lang will be passed to the `inline()` function and to the `run()` function and shared among the classes' methods as parameter (ugly as fuck but I don't know what else to do)
  
  - [ ] "auto" should rely on `User.language_code` or "en"
  
  - [ ] warn directly log chats on `Users.lang()` if a string is missing
  
  - [ ] adding missing strings:
    
    - [ ] info.py
    
    - [ ] encode.py
    
    - [ ] score.py
  
  - [ ] `/translate` (sync with settings)

- [ ] revise `/hey` (to turn into `/forward` or `/support`)
  
  - [ ] enable chat forward: every message sent is forwarded (`hey_admins.parse()` will check if forward is enabled in `self.usr`)
  
  - [x] enable media forward from admin's chats (done by using `copy_message()`)
  
  - [x] set support chat
  
  - [x] warn other support chats who replied

- [ ] replace `/admin` command with dot-commands (`.add` instead of `/admin add` and so on, only admin/support/log chats)
  
  - [ ] `.send chat_id message` command
