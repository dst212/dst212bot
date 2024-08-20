import logging


class init:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    @property
    def name(self):
        return self._name

    @property
    def flag(self):
        return self._flag

    def string(self, string):
        try:
            return self.__getattribute__(string)
        except AttributeError:
            self.log.warn(f"String not found: {string}")
            return f"{string}"

    @property
    def __dict__(self):
        return dict(flag=self._flag, name=self._name)

    _name = "English"
    _flag = "🇬🇧"

    # Strings
    YES = "Yes"
    NO = "No"
    IM_SMORT = "I'm SmOrT!!!!!!"
    # specific messages
    WELCOME_MESSAGE = "Welcome, {}.\nTo get a list of available commands send /help.\nTo customize your preferences send /settings."
    HI_THERE_ADMIN = "Hi there {}, at your service."
    HI_THERE_USER = "Hi there {}, you can start me privately, I'll wait for you there :)"
    LETS_START = "Let's start!"
    CREDITS_MESSAGE = """
<b>Credits</b>

Bot written in Python by @dst212.
https://dst212.github.io/

News channel: @dst212botnews

<b>Libraries</b>
- <code>pyrogram</code>: Telegram client
- <code>opencv-python</code>: QR code detection and decoding
- <code>pyqrcode</code>: QR code generation
- <code>py-googletrans</code> (<a href="https://github.com/bllendev/py-googletrans">GitHub repo</a>): Translation APIs
- <code>gtts</code>: Text to speech APIs
- <code>psutil</code>: processes info gathering

<b>Data sources</b>
- <i>Reverse Dictionary</i>: https://reversedictionary.org
- <i>Pokémon</i>: https://pokeapi.co/
"""
    # generic words and placeholders
    ERROR = "Error"
    EXAMPLE = "Example"
    ALIASES = "Aliases"
    RESULT = "Result"
    RESULTS = "Results"
    TOTAL = "Total"
    USAGE = "Usage"
    SYNTAX = "Syntax"
    HELP = "Help"
    BACK = "Back"
    CLOSE = "Close"
    UNKNOWN = "Unknown"
    AVAILABLE_CATEGORIES = "Available categories"
    # notices
    INLINE_MODE_NOTICE = "In inline-mode, just write the commands without the slash <code>/</code> and always provide an input text."
    CHOOSE_A_BUTTON = "Choose a button to get info about that command."
    DOWNLOADING = "Downloading..."
    UPLOADING = "Uploading..."
    LOADING = "Loading..."
    PROCESSING = "Processing..."
    CREATING = "Creating..."
    RESTARTING_BOT = "Restarting the bot..."
    FETCHING_DATA = "Fetching data..."
    CLICK_HERE_TO_BE_RETARDED = "Click here to be retarded."
    WRITE_SOME_TEXT = "Write some text."
    # generic warnings
    LOL_NO_THANKS = "Lol no thanks."
    WE_ALL_KNOW_THAT = "We all know that."
    REPEAT_WHAT = "Repeat what?"
    MY_JOB_HERE_IS_DONE = "My job here is done.\n\n<i>*swoosh*</i>"
    AN_ERROR_OCCURRED = "An error occurred."
    ERROR_OCCURRED = "An error occurred."
    AN_ERROR_OCCURRED_WHILE_PERFORMING = "An error occurred while performing this operation.\nContact @dst212 for further information."
    NO_RESULTS = "No results."
    NO_RESULTS_FOR = "No results for {}."
    DOESNT_EXIST = "{} doesn't exist."
    INVALID_SYNTAX = "Invalid syntax."
    INVALID_USAGE = "Invalid usage."
    PROVIDE_TEXT = "Provide some text by replying to a message or writing it alongside the command."
    PROVIDE_SEARCH_QUERY = "Provide a search query."
    COULDNT_FIND_SECTION = "Couldn't find the section {}."
    ERROR_WHILE_CREATING_FILE = "Error while creating the file."
    NOT_AVAILABLE_AT_THIS_TIME = "Not available at this time."
    IS_NOT_AVAILABLE_AT_THIS_TIME = "{} is not available at this time."
    PICK_RANDOM_REPLY_TO_A_MESSAGE = "To use this command, reply to a message with more than one line.\nThe bot will pick one (or more).\n<code>/help pickrandom</code> for more info."
    IS_INVALID_USING = "<code>{}</code> is not a valid value, using <code>{}</code>."
    NO_ENTRY = "No entry."
    NO_ENTRY_FOR = "No entry for {}."
    NO_PERMISSIONS = "You have no permissions to perform this operation."
    NOT_RECOGNIZED = "{} not recognized."
    NOTHING_CHANGED = "Nothing changed."
    LANGUAGE_IS_NOT_SUPPORTED = "Language <code>{}</code> not supported."
    USING_LANGUAGE = "Using language <code>{}</code>."
    INVALID_COMMAND = "<code>{}</code> is not a valid command."
    UNNEEDED_ARGUMENT = "Unneded arguments."
    WEBSITE_UNAVAILABLE = "Website unavailable."
    PROVIDE_USERNAME_OR_ID = "Provide a valid username or id."
    YOU_SHOULD_KNOW = "You should know it..."
    # generic info
    RESULTS_FOR = "Result for {}"
    TRANSLATE_FROM_TO = "Translate {}from {} to {}"
    FILE_SAVED = "Saved {}."
    CATEGORY_DOESNT_EXIST = "The specified category doesn't exist."
    IT_DOESNT_EXIST = "The category {} doesn't exist."
    DID_YOU_MEAN = "Did you mean {}?"
    # settings
    SETTINGS_FOR_THIS_CHAT = "Here you can change the settings for this chat."
    SETTINGS_OVERRIDE = "Override groups' settings"
    SETTINGS_AUTO_TR = "Auto-translate messages"
    SETTINGS_TR_COMMANDS = "Translate commands"
    SETTINGS_SELECT_VALUE = "Select a new value for <code>{}</code>. Current value is <code>{}</code>."
    SETTINGS_NOT_VALID_VALUE_FOR = "<code>{}</code> is not a valid value for <code>{}</code>."
    SETTINGS_SET_TO = "<code>{}</code> set to <code>{}</code> (it was <code>{}</code>)."
    SETTINGS_COULD_NOT_SET = "Could not set <code>{}</code> to <code>{}</code> (it's <code>{}</code> now)."
    MUST_BE_ADMIN = "You must be admin to perform this action."
    SETTINGS_HELP = """
<b>Commands:</b>

<code>/settings</code>
Open settings menu.

<code>/settings get</code>
Receive a <code>json</code> file containing current chat's settings.

<code>/settings set &lt;item&gt; &lt;value&gt;</code>
Set <code>&lt;item&gt;</code> to <code>&lt;value&gt;</code>.

<b>Options:</b>
- <code>lang</code> (language): the language the bot will use replying to you.
- <code>override</code> (override groups' settings, private): when on, the bot ignores groups' language and uses the language set privately.
- <code>auto-tr</code> (auto translate, groups only): when on, the bot translates messages sent by group's users if necessary.
- <code>fwd</code> (chat forward): forward messages in this chat to support volunteers, instead of using the /hey command each time.
"""
    # encode
    ENCODE_FROM_TO = "Encode {}from {} to {}"
    ENCODE_ERROR = "An error occurred, ensure the input text is correctly encoded."
    ENCODE_PROVIDED_ISNT = "The provided text's encoding isn't <code>{}</code>."
    ENCODE_IS_NOT_VALID = "<code>{}</code> is not a valid encoding."
    ENCODE_ARE_NOT_VALID = "<code>{}</code> and <code>{}</code> are not valid encodings."
    PROVIDE_DECODING_ENCODING_TEXT = "Provide a decoding format, an encoding format and a text to parse."
    # translate
    TRANSLATION_TITLE = "Translation"
    SOURCE_TEXT = "Source text"
    # QRCode
    QR_CODE_EMPTY = "The content was either empty or OpenCV didn't catch it."
    QR_CODE_NOT_FOUND = "No QR codes were detected in that image."
    QR_CODE_DETECTING = "Detecting and decoding QR Code..."
    # score
    SCORE_HELP = """
<code>/score</code> - Manage scores on the current chat.
A score is a set of items for which is kept a integer value each.

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
"""
    SCORE_HELP_ADD = "<code>/score add score_name item_name [value=1]</code>\n\nIncrement by <code>value</code> the item <code>item_name</code> of <code>score_name</code>.\nYou may use negative values as <code>value</code>."
    SCORE_HELP_SET = "<code>/score set score_name item_name [value=1]</code>\n\nSet to <code>value</code> the item <code>item_name</code> of <code>score_name</code>."
    SCORE_HELP_SETRAW = "<code>/score setraw score_name\nitem1 : value\nitem2 : value\nitem3 : value</code>\n\nFor each new line, create a item and assign the specified value to it."
    SCORE_INVALID_NAME = "Invalid score name: must be alphanumeric (dashes <code>-</code> and unsersocres <code>_</code> are allowed)."
    SCORE_PROVIDE_NAME = "Provide a valid name for the score."
    SCORE_PROVIDE_ITEM_NAME = "Provide a valid name for the item."
    SCORE_DOESNT_EXIST = "The score <b>{}</b> doesn't exist."
    SCORE_CREATED_SUCCESSFULLY = "The score <b>{}</b> was created sccessfully."
    SCORE_ALREADY_EXISTS = "The score <b>{}</b> already exists."
    SCORE_WAS_NOW_GONE = "The score was:\n\n{}\n\nNow it's gone."
    SCORE_WAS = "The score was:\n\n{}"
    SCORE_NOW_ITS = "Now it's:\n\n{}"
    SCORE_RENAMED_FROM = "The score <b>{}</b> was renamed to <b>{}</b>."
    SCORE_YOU_ARENT_AN_EDITOR = "You aren't an editor for this score."
    SCORE_YOU_ARENT_THE_OWNER = "You aren't the owner this score."
    SCORE_ITEM_SET_TO = "<i>{}</i> of <b>{}</b> was set to <code>{}</code>."
    SCORE_NO_ITEMS = "No items in this score at the moment."
    SCORE_ITEM_DOESNT_EXIST = "The item <i>{}</i> doesn't exist in <b>{}</b>."
    SCORE_ITEM_DELETED = "The item <i>{}</i> in <b>{}</b> was deleted."
    SCORE_ONLY_NUMBERS = "Only integers are accepted as values for the items."
    SCORE_DISPLAY_SET = "The score <b>{}</b> will now be displayed as <b>{}</b>."
    SCORE_UNNEEDED_ARGUMENT = "Unneeded arguments."
    # counter
    COUNTER_HELP = """
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
Display the counter and its value.

<code>/counter set counter_name value</code>
Set a counter to a certain value.

<code>/counter add counter_name [value=1]</code>
Add a cerain value to a counter.

<code>/counter auto add/del counter_name filter</code>
Add/delete a filter to a counter (auto mode).
If a sent message contains the filter, the counter will be updated.
"""
    COUNTER_IS = "<b>{}</b> is set to <code>{}</code>."
    COUNTER_SET = "<b>{}</b> set to <code>{}</code>."
    COUNTER_ALREADY_EXISTS = "The counter already exists."
    COUNTER_COULDNT_CREATE = "Couldn't create that counter."
    COUNTER_CREATED = "Counter created."
    COUNTER_YOU_ARENT_THE_OWNER = "You arent the owner of that counter."
    COUNTER_YOU_ARENT_AN_EDITOR = "You arent an editor of that counter."
    COUNTER_DOESNT_EXIST = "<b>{}</b> doesn't exist."
    COUNTER_DELETED = "<b>{}</b> was deleted (its value was <code>{}</code>)."
    COUNTER_RENAMED_FROM = "<b>{}</b> was renamed to <b>{}</b>."
    COUNTER_DISPLAY_SET = "<b>{}</b> will now be displayed as <b>{}</b>."
    COUNTER_AUTO_HAS = "<b>{}</b> has now the following triggers:\n<i>{}</i>"
    COUNTER_WORD_NOT_FOUND = "<i>{}</i> is not among the triggers:\n<i>{}</i>"
    COUNTER_PROVIDE_NAME = "Provide a valid name for the counter.\nOnly letters, digits, dashes and underscores (<code>-</code> and <code>_</code>) are allowed."
    COUNTER_NO_TRIGGERS = "No triggers at the moment."
    COUNTER_ONLY_NUMBERS = "You can only set numbers."
    # Other commands
    SHUFFLE_TEXT = "Shuffle text"
    ################
    #   COMMANDS   #
    ################
    COMMANDS = {
        "help": "Get info about <code>command</code>.\nOmit <code>command</code> to get a list of available commands.",
        "settings": "Change preferences for the current chat.\n<code>/settings get</code> to get a json file containing the settings (occasional debugging).\n<code>/settings set &lt;item&gt; &lt;value&gt;</code> to change a specific option quickly.",
        "translate": 'Translate <code>text</code> from <code>from_lang</code> to <code>to_lang</code>.\n<code>from_lang</code> and <code>to_lang</code> must be either "auto" or a valid language identifier (such as <i>en</i>, <i>it</i>, <i>de</i>...).\nUsing the alias <code>/tr</code>, the result is shown directly and not verbosely.\n<code>text</code> may be omitted if replying to a message.',
        "tts": "Text to speech, turn <code>text</code> into speech and get an <code>mp3</code> file.\n<code>text</code> may be omitted if replying to a message.",
        "qr": "Create a QR code from <code>text</code>.\nTo decode a QR code reply to a photo containing it omitting <code>text</code>.",
        "wordfor": "Get the word defining <code>definition</code> through Reverse Dictionary.",
        "encode": "Encode text from <code>x</code> to <code>y</code>.\nAccepted values for x and y:\n- text, txt, t\n- binary, bin, b\n- base64, b64\n<code>text</code> may be omitted if replying to a message.",
        "pokemon": "Get data about <code>name</code> of <code>category</code>.\nYou may directly look for an item without specifying any category (for example <code>/pokemon ditto</code> is the same as <code>/pokemon pokemon ditto</code>).\nSend <code>/pokemon</code> to get a list of availble categories through the bot.",  # provided categories by the PokeAPI.\nNot every category is available through the bot."
        "score": "Create and edit scores on the current chat. <code>/score help</code> for details.",
        "counter": "Create and edit counters on the current chat. <code>/counter help</code> for details.",
        "random": "Generate a random number from <code>x</code> (default is 0) to <code>y</code> (default is 100).",
        "pickrandom": "Replying to a message written on multiple lines with this command, one or more lines (<code>limit</code>, default is 1) will be picked up randomly.",
        "shuffle": "Shuffle <code>text</code>'s letters.\n<code>text</code> may be omitted if replying to a message.",
        "imdumb": "Make <code>text</code> written like if you were dumb. <code>text</code> may be omitted if replying to a message.",
        "say": "Make the bot say <code>text</code>.",
        "len": "Get <code>text</code>'s length.\n<code>text</code> may be omitted if replying to a message.",
    }
    QUERY_COMMANDS = {
        "translate": """Translate "text" from "from_lang" to "to_lang".""",
        "imdumb": """Write messages like if you were stupid.""",
        "encode": """Convert "text" from "x" encoding to "y" encoding.""",
        "pokemon": """Search "name" as a "category" at PokeAPI.""",
        "wordfor": """Get the word for "definition" through the Reverse Dictionary.""",
    }
    QUERY = {
        "help": {
            "title": "Help about commands",
            "content": "To get help, start the bot privately and send /help.",
            "description": "Start the bot in privately to get help.",
        }
    }
