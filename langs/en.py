name = "English"
strings = {
"YES": "Yes",
"NO": "No",
"IM_SMORT": "I'm SmOrT!!!!!!",

# specific messages
"WELCOME_MESSAGE": "Welcome, {}.\nTo get a list of available commands send /help.",
"CREDITS_MESSAGE": f"""
<b>Credits</b>

Bot written in Python by @dst212.
https://dst212.github.io/

<b>Libraries</b>
- <code>pyrogram</code>: Telegram client
- <code>opencv-python</code>: QR code detection and decoding
- <code>pyqrcode</code>: QR code generation
- <code>googletrans</code> (3.1.0a0): Translation APIs
- <code>gtts</code>: Text to speech APIs

<b>Data sources</b>
- <i>Reverse Dictionary</i>: https://reversedictionary.org
- <i>Pokémon</i>: https://pokeapi.co/
- <i>Pokémon GO</i>: https://pokemondb.net/
""",
# - <code>pypng</code>: support library for <code>pyqrcode</code>
# - <code>pandas</code>: HTML manipulation
# - <code>beautifulsoup4</code>: HTML manipulation

# generic words and placeholders
"ERROR": "Error",
"EXAMPLE": "Example",
"ALIASES": "Aliases",
"RESULTS": "Results",
"USAGE": "Usage",
"SYNTAX": "Syntax",
"HELP": "Help",
"BACK": "Back",
"AVAILABLE_CATEGORIES": "Available categories",

# titles
"TRANSLATION_TITLE": "Translation",

# notices
"INLINE_MODE_NOTICE": "In inline-mode, just write the commands without the slash <code>/</code> and always provide an input text.",
"CHOOSE_A_BUTTON": "Choose a button to get info about that command.",
"DOWNLOADING": "Downloading...",
"LOADING": "Loading...",
"RESTARTING_BOT": "Restarting the bot...",
"FETCHING_DATA": "Fetching data...",
"CLICK_HERE_TO_BE_RETARDED": "Click here to be retarded",

# generic warnings
"LOL_NO_THANKS": "Lol no thanks.",
"AN_ERROR_OCCURRED": "An error occurred.",
"ERROR_OCCURRED": "An error occurred.",
"AN_ERROR_OCCURRED_WHILE_PERFORMING": "An error occurred while performing this operation.\nContact @dst212 for further information.",
"NO_RESULTS": "No results.",
"NO_RESULTS_FOR": "No results for {}.",
"DOESNT_EXIST": "{} doesn't exist.",
"INVALID_SYNTAX": "Invalid syntax.",
"INVALID_USAGE": "Invalid usage.",
"PROVIDE_TEXT": "Provide some text by replying to a message or writing it alongside the command.",
"PROVIDE_SEARCH_QUERY": "Provide a search query.",
"COULDNT_FIND_SECTION": "Couldn't find the section {}.",
"ERROR_WHILE_CREATING_FILE": "Error while creating the file.",
"NOT_AVAILABLE_AT_THIS_TIME": "Not available at this time.",
"IS_NOT_AVAILABLE_AT_THIS_TIME": "{} is not available at this time.",
"PICK_RANDOM_REPLY_TO_A_MESSAGE": "Reply to the message containing a lilst of items (one for each line).",
"IS_INVALID_USING": "<code>{}</code> is not a valid value, using <code>{}</code>.",
"NO_ENTRY_FOR": "No entry for {}.",
"NO_PERMISSIONS": "You have no permissions to perform this operation.",
"LANGUAGE_IS_NOT_SUPPORTED": "Language <code>{}</code> not supported.",
"USING_LANGUAGE": "Using language <code>{}</code>.",

"INVALID_COMMAND": "<code>{}</code> is not a valid command.",
"UNNEEDED_ARGUMENT": "Unneded arguments.",
"WEBSITE_UNAVAILABLE": "Website unavailable.",
"PROVIDE_DECODING_ENCODING_TEXT": "Provide a decoding format, an encoding format and a text to parse.",
"PROVIDE_USERNAME_OR_ID": "Provide a valid username or id.",
"YOU_SHOULD_KNOW": "You should know it..",

# generic info
"RESULTS_FOR": "Result for {}",
"ENCODE_FROM_TO": "Encode {}from {} to {}",
"TRANSLATE_FROM_TO": "Translate {}from {} to {}",
"FILE_SAVED": "Saved {}.",
"CATEGORY_DOESNT_EXIST": "The specified category doesn't exist.",
"IT_DOESNT_EXIST": "The category {} doesn't exist.",
"DID_YOU_MEAN": "Did you mean {}?",

# settings
"SETTINGS_FOR_THIS_CHAT": "Here you can change the settings for this chat.",
"SETTINGS_OVERRIDE": "Override groups' settings",
"SETTINGS_SYNC-TR": "Sync language with /translate",

# QRCode
"QR_CODE_EMPTY": "The content was either empty or OpenCV didn't catch it.",
"QR_CODE_NOT_FOUND": "No QR codes were detected in that image.",
"QR_CODE_DETECTING": "Detecting and decoding QR Code...",

# score
"SCORE_HELP": f"""
<code>/score</code> - Manage scores on the current chat.
A score is a set of items for which is kept a integer value.

<b>Usage:</b>

<code>/score new/create score_name</code>
Create a new score for the current chat.

<code>/score del/delete/remove score_name [other scores]</code>
Delete a score (or more than one) in the current chat.

<code>/score ren/rename score_name new_name</code>
Rename a score. This won't change it's display name.

<code>/score display score_name display_name</code>
Set a display name for a score. This won't rename the score.

<code>/score get/print score_name</code>
Display the score with its items and the related values.

<code>/score set score_name item_name [value=1]</code>
Set a value for the specified item.
The item is create if it doesn't exist and value is not equal to <code>0</code>.
Setting the value to <code>0</code> deletes the item if it exists.

<code>/score add score_name item_name [value=1]</code>
Increment an item's value by the specified value.
If the new value is <code>0</code>, the item is kept anyway.

<code>/score delitem score_name item_name</code>
Alias for <code>/score set score_name item_name 0</code>.

<pre>/score setraw score_name
item1 : value1
item2 : value2
item3:value3
item4 :value4
[...]</pre>
Replace the items for an existing score with the specified ones.
This is useful to clone or merge different scores, or create more items on the fly on a new score.
""",
"SCORE_INVALID_NAME": "Invalid score name: must be alphanumeric (dashes <code>-</code> and unsersocres <code>_</code> are allowed).",
"SCORE_PROVIDE_NAME": "Provide a valid name for the score.",
"SCORE_PROVIDE_ITEM_NAME": "Provide a valid name for the item.",
"SCORE_DOESNT_EXIST": "The score <b>{}</b> doesn't exist.",
"SCORE_CREATED_SUCCESSFULLY": "The score <b>{}</b> was created sccessfully.",
"SCORE_ALREADY_EXISTS": "The score <b>{}</b> already exists.",
"SCORE_WAS_NOW_GONE": "The score was:\n\n{}\n\nNow it's gone.",
"SCORE_WAS": "The score was:\n\n{}",
"SCORE_NOW_ITS": "Now it's:\n\n{}",
"SCORE_RENAMED_FROM": "The score <b>{}</b> was renamed to <b>{}</b>.",
"SCORE_YOU_ARENT_AN_EDITOR": "You aren't an editor for this score.",
"SCORE_YOU_ARENT_THE_OWNER": "You aren't the owner this score.",
"SCORE_ITEM_SET_TO": "<i>{}</i> of <b>{}</b> was set to <code>{}</code>.",
"SCORE_NO_ITEMS": "No items in this score at the moment.",
"SCORE_ITEM_DOESNT_EXIST": "The item <i>{}</i> doesn't exist in <b>{}</b>.",
"SCORE_ITEM_DELETED": "The item <i>{}</i> in <b>{}</b> was deleted.",
"SCORE_ONLY_NUMBERS": "Only integers are accepted as values for the items.",
"SCORE_DISPLAY_SET": "The score <b>{}</b> will now be displayed as <b>{}</b>.",
"SCORE_UNNEEDED_ARGUMENT": "Unneeded arguments.",

# counter
"COUNTER_HELP": f"""
<code>/counter</code> - Manage counters on the current chat.
A counter stores a value which can be incremented manually or automatically when someone writes something.

<b>Usage:</b>

<code>/counter new/create counter_name</code>
Create a new counter for the current chat.

<code>/counter del/delete/remove counter_name</code>
Delete a counter in the current chat.

<code>/counter ren/rename counter_name new_name</code>
Rename a counter. This won't change it's display name.

<code>/counter display counter_name display_name</code>
Set a display name for a counter. This won't rename the counter.

<code>/counter get/print counter_name</code>
Display the counter with its items and the related values.

<code>/counter set counter_name value</code>
Set a counter to a certain value.

<code>/counter add counter_name [value=1]</code>
Add a cerain value to a counter.

<code>/counter auto add/del counter_name filter</code>
Add/delete a filter to a counter (auto mode).
If the filter appears in a message, the counter will be updated.
""",
"COUNTER_IS": "<b>{}</b> is set to <code>{}</code>.",
"COUNTER_SET": "<b>{}</b> set to <code>{}</code>.",
"COUNTER_ALREADY_EXISTS": "The counter already exists.",
"COUNTER_COULDNT_CREATE": "Couldn't create that counter.",
"COUNTER_CREATED": "Counter created.",
"COUNTER_YOU_ARENT_THE_OWNER": "You arent the owner of that counter.",
"COUNTER_YOU_ARENT_AN_EDITOR": "You arent an editor of that counter.",
"COUNTER_DOESNT_EXIST": "<b>{}</b> doesn't exist.",
"COUNTER_DELETED": "<b>{}</b> was deleted (its value was <code>{}</code>).",
"COUNTER_RENAMED_FROM": "<b>{}</b> was renamed to <b>{}</b>.",
"COUNTER_DISPLAY_SET": "<b>{}</b> will now be displayed as <b>{}</b>.",
"COUNTER_AUTO_HAS": "<b>{}</b> has now the following triggers:\n<i>{}</i>",
"COUNTER_WORD_NOT_FOUND": "<i>{}</i> is not among the triggers:\n<i>{}</i>",
"COUNTER_PROVIDE_NAME": "Provide a valid name for the counter.\nOnly letters, digits, dashes and underscores (<code>-</code> and <code>_</code>) are allowed.",
"COUNTER_NO_TRIGGERS": "No triggers at the moment.",
"COUNTER_ONLY_NUMBERS": "You can only set numbers.",

# pokemon go
"POGO_HELP": """
<code>/pogo</code> - Game data about Pokémon GO.

<b>Usage:</b>
<code>/pogo command [arguments]</code>
Perfom a specific action (<code>command</code>).
The <code>arguments</code> are defined by the <code>command</code> itself.

<b>Commands:</b>

<code>/pogo rank pokemon_name atk.def.hp [max_cp=1500] [min_iv=0] [max_lvl=50]</code>
Get the rank of a Pokémon given its IVs.
 - <code>pokemon_name</code>: name for the mon to analyse.
 - <code>atk.def.hp</code>: mon's stats, from <code>0</code> to <code>15</code>.
 - <code>max_cp</code>: league's cap, default is <code>1500</code> (Great League).
 - <code>min_iv</code>: minimum IVs to consider, default is <code>0</code> (wild catch).
 - <code>max_lvl</code>: maximum level to consider, default is <code>50</code> (XL Pokémon).
Examples:
 <code>/pogo rank umbreon 15.15.15 2500 0 51</code>
 <code>/pogo rank talonflame 0.15.14</code>
 <code>/pogo rank pikachu 5/15/14 500</code>

<code>/pogo iv pokemon_name rank [max_cp=1500] [min_iv=0] [max_lvl=50]</code>
Get IVs of a Pokémon given its rank.
Arguments as above, except for:
 - <code>rank</code>: the rank of the pokemon, must be an integer between 1 and 4096.
Examples:
 <code>/pogo iv medicham 1 1500 0 51</code>
 <code>/pogo iv talonflame 1 2500</code>
 <code>/pogo iv deoxys defense forme 1 1500 10</code>

In inline mode, commands are the same:
 <code>@dst212bot pogo iv umbreon 1</code>
is the same as:
 <code>/pogo iv umbreon 1</code>

The PokéDex refers to <a href="https://pokemondb.net/go/pokedex">PokemonDB</a>'s data.
""",
"POGO_INVALID_USAGE": "Invalid usage.\nSend <code>/pogo help</code> to get usage details.",
"POGO_IV_MUST_BE_BETWEEN": "Invalid data: IVs must be 3 integer numbers between 0 and 15.",
"POGO_RANK_MUST_BE_INTEGER": "Invalid data: rank must be an integer between 1 and 4096.",
"POGO_ENSURE_DATA_IS_CORRECT": "Invalid data: ensure everything is correct. Send <code>/pogo help</code> to get usage details.",

# Other commands
"SCRAMBLE_TEXT": "Scramble text",

################
### COMMANDS ###
################

"COMMANDS": {
	"help": {
		"args": ["[command]"],
		"desc": "Get info about <code>command</code>.\nOmit <code>command</code> to get a list of available commands.",
	},
	"translate": {
		"args": ["from_lang", "to_lang", "[text]"],
		"aliases": "tr",
		"desc": "Translate <code>text</code> from <code>from_lang</code> to <code>to_lang</code>.\n<code>from_lang</code> and <code>to_lang</code> must be either \"auto\" or a valid language identifier (such as <i>en</i>, <i>it</i>, <i>de</i>...).\nUsing the alias <code>/tr</code>, the result is shown directly and not verbosely.\n<code>text</code> may be omitted if replying to a message.",
	},
	"tts": {
		"args": ["[text]"],
		"desc": "Text to speech, turn <code>text</code> into speech and get an <code>mp3</code> file.\n<code>text</code> may be omitted if replying to a message.",
	},
	"qr": {
		"args": ["[text]"],
		"desc": "Create a QR code from <code>text</code>.\nTo decode a QR code reply to a photo containing it omitting <code>text</code>.",
	},
	"encode": {
		"args": ["x", "y"],
		"aliases": ["e"],
		"desc": "Encode text from <code>x</code> to <code>y</code>.\nAccepted values for x and y:\n- text, txt, t\n- binary, bin, b\n- base64, b64\n<code>text</code> may be omitted if replying to a message.",
		"examples" : ["text binary henlo uorld", "b64 t Q2lhbw=="],
	},
	"pokemon": {
		"args": ["category", "name"],
		# "aliases": ["p"],
		"desc": "Get data about <code>name</code> of <code>category</code>.\nSend /pokemon to get a list of availble categories through the bot.",#provided categories by the PokeAPI.\nNot every category is available through the bot.",
		"examples" : ["pokemon eevee", "move quick attack"],
	},
	"pogo": {
		"args": ["command", "arguments"],
		"desc": "Get data about Pokémon GO stuff. <code>/pogo help</code> for details.",
	},
	"score": {
		"args": ["command", "arguments"],
		"desc": "Create and edit scores on the current chat. <code>/score help</code> for details.",
	},
	"counter": {
		"args": ["command", "arguments"],
		"desc": "Create and edit counters on the current chat. <code>/counter help</code> for details.",
	},
	"random": {
		"args": ["[x]", "[y]"],
		"aliases": ["r"],
		"desc": "Generate a random number from <code>x</code> (default is 0) to <code>y</code> (default is 100).",
	},
	"pickrandom": {
		"args": ["[limit]"],
		"aliases": ["pr"],
		"desc": "Pick one or more (<code>limit</code>, default is 1) random items from a list.\nThe list must be provided from a previously written message with one item per line.\nSend the command replying to that message to pick the items.",
	},
	"scramble": {
		"args": ["[text]"],
		"desc": "Scramble <code>text</code>'s content.\n<code>text</code> may be omitted if replying to a message.",
	},
	"len": {
		"args": ["[text]"],
		"desc": "Get <code>text</code>'s length.\n<code>text</code> may be omitted if replying to a message.",
	},
	"count": {
		"args": [],
		"desc": "Count the messages in a chat.\nIf replying to a message, the count starts from there.",
	},
	"info": {
		"args": ["[username/id]"],
		"desc": "Get info about an user by replying to their message.",
	},
},
"QUERY_COMMANDS": {
	"translate": {
		"syntax": "translate from_lang to_lang text",
		"description": """Translate "text" from "from_lang" to "to_lang".""",
		"example": "translate auto it hello darkness my old friend",
	},
	"info": {
		"syntax": "info username/id",
		"description": """Get info about an user on Telegram""",
		"example": "info @dst212bot",
	},
	"imdubm": {
		"syntax": "imdumb text",
		"description": """Write messages like you were stupid""",
		"example": "imdumb im super smort",
	},
	"encode": {
		"syntax": "encode x y text",
		"description": """Convert "text" from "x" encoding to "y" encoding.""",
		"example": "encode text base64 henlo world",
	},
	"pokemon": {
		"syntax": "pokemon category name",
		"description": """Search "name" as a "category" at PokeAPI.""",
		"example": "pokemon pokemon eevee",
	},
	"wordfor": {
		"syntax": "wordfor definition",
		"description": """Get the word for "definition" through the Reverse Dictionary.""",
		"example": "wordfor the fear of high places",
	},
},
"QUERY": {
	"help": {
		"title": "Help about commands",
		"content": "To get help, start the bot privately and send /help.",
		"description": "Start the bot in privately to get help."
	},
},
}