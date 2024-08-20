from . import en


class init(en.init):
    _name = "Italiano"
    _flag = "🇮🇹"

    # Strings
    YES = "Sì"
    NO = "No"
    IM_SMORT = "SoNo InTeLlIgEnTe!!!!!!"
    # specific messages
    WELCOME_MESSAGE = "Benvenutə, {}.\nPer vedere i comandi disponibili, invia /help.\nPer personalizzare le tue preferenze, invia /settings."
    HI_THERE_ADMIN = "Ehilà {}, al tuo servizio."
    HI_THERE_USER = "Ehilà {}, puoi avviarmi in privato, ti aspetterò lì :)"
    LETS_START = "Iniziamo!"
    CREDITS_MESSAGE = """
<b>Crediti</b>

Bot scritto in Python da @dst212.
https://dst212.github.io/

Canale delle notizie: @dst212botnews

<b>Librerie</b>
- <code>pyrogram</code>: client Telegram
- <code>opencv-python</code>: rilevamento e lettura codici QR
- <code>pyqrcode</code>: generazione codici QR
- <code>py-googletrans</code> (<a href="https://github.com/bllendev/py-googletrans">repo GitHub</a>): API per il traduttore
- <code>gtts</code>: API per il text-to-speech
- <code>psutil</code>: raccolta info processi

<b>Risorse dati</b>
- <i>Reverse Dictionary</i>: https://reversedictionary.org
- <i>Pokémon</i>: https://pokeapi.co/
"""
    # generic words and placeholders
    ERROR = "Errore"
    EXAMPLE = "Esempio"
    ALIASES = "Alias"
    RESULT = "Risultato"
    RESULTS = "Risultati"
    TOTAL = "Totale"
    USAGE = "Utilizzo"
    SYNTAX = "Sintassi"
    HELP = "Aiuto"
    BACK = "Indietro"
    CLOSE = "Chiudi"
    UNKNOWN = "Sconosciuto"
    AVAILABLE_CATEGORIES = "Categorie disponibili"
    # notices
    INLINE_MODE_NOTICE = "Nella modalità inline, scrivi i comandi senza la slash <code>/</code> e inserisci sempre il testo di input."
    CHOOSE_A_BUTTON = "Premi un pulsante per avere informazioni sul comando corrispondente."
    DOWNLOADING = "Scaricando..."
    UPLOADING = "Caricando..."
    LOADING = "Caricamento..."
    PROCESSING = "Processando..."
    CREATING = "Creazione..."
    RESTARTING_BOT = "Riavviando il bot..."
    FETCHING_DATA = "Recupero dati..."
    CLICK_HERE_TO_BE_RETARDED = "Clicca qui per essere ritardato"
    WRITE_SOME_TEXT = "Scrivi del testo."
    # generic warnings
    LOL_NO_THANKS = "Lol no grazie."
    WE_ALL_KNOW_THAT = "Lo sappiamo tutti."
    REPEAT_WHAT = "Ripetere cosa?"
    MY_JOB_HERE_IS_DONE = "Il mio lavoro qui è finito.\n\n<i>*swoosh*</i>"
    AN_ERROR_OCCURRED = "È avvenuto un errore."
    ERROR_OCCURRED = "È avvenuto un errore."
    AN_ERROR_OCCURRED_WHILE_PERFORMING = "È avvenuto un errore durante l'esecuzione di questa operazione.\nContatta @dst212 per ulteriori informazioni."
    NO_RESULTS = "Nessun risultato."
    NO_RESULTS_FOR = "Nessun risultato per {}."
    DOESNT_EXIST = "{} non esiste."
    INVALID_SYNTAX = "Sintassi non valida."
    INVALID_USAGE = "Utilizzo non valido."
    PROVIDE_TEXT = "Fornisci del testo rispondendo ad un messaggio o scrivendolo accanto al comando."
    PROVIDE_SEARCH_QUERY = "Fornisci una stringa di ricerca."
    COULDNT_FIND_SECTION = "Impossibile trovare la sezione {}."
    ERROR_WHILE_CREATING_FILE = "Errore nella creazione del file."
    NOT_AVAILABLE_AT_THIS_TIME = "Non disponibile al momento."
    IS_NOT_AVAILABLE_AT_THIS_TIME = "{} non è al momento disponibile."
    PICK_RANDOM_REPLY_TO_A_MESSAGE = "Per usare questo comando, rispondi ad un messaggio con più di una riga.\nIl bot ne sceglierà una (o più).\n<code>/help pickrandom</code> per ulteriori informazioni."
    IS_INVALID_USING = "<code>{}</code> non è un valore valido, verrà usato <code>{}</code>."
    NO_ENTRY = "Nessuna voce."
    NO_ENTRY_FOR = "Nessuna voce per {}."
    NO_PERMISSIONS = "Non hai i permessi per effettuare questa operazione."
    NOT_RECOGNIZED = "{} non riconosciuto."
    NOTHING_CHANGED = "Non è cambiato nulla."
    LANGUAGE_IS_NOT_SUPPORTED = "La lingua <code>{}</code> non è supportata."
    USING_LANGUAGE = "Verrà usata la lingua <code>{}</code>."
    INVALID_COMMAND = "<code>{}</code> non è un comando valido."
    UNNEEDED_ARGUMENT = "Ci sono argomenti non necessari."
    WEBSITE_UNAVAILABLE = "Sito non disponibile."
    PROVIDE_USERNAME_OR_ID = "Fornisci un username o un id valido."
    YOU_SHOULD_KNOW = "Dovresti saperlo..."
    # generic info
    RESULTS_FOR = "Risultati per {}"
    TRANSLATE_FROM_TO = "Traduci {}da {} a {}"
    FILE_SAVED = "Salvato {}."
    CATEGORY_DOESNT_EXIST = "La categoria specificata non esiste."
    IT_DOESNT_EXIST = "La categoria {} non esiste."
    DID_YOU_MEAN = "Intendevi {}?"
    # settings
    SETTINGS_FOR_THIS_CHAT = "Qui si può cambiare le impostazioni per questa chat."
    SETTINGS_OVERRIDE = "Sovrascrivi impostazioni gruppi"
    SETTINGS_AUTO_TR = "Auto-traduci i messaggi"
    SETTINGS_TR_COMMANDS = "Traduci i comandi"
    SETTINGS_SELECT_VALUE = "Scegli un nuovo valore per <code>{}</code>. Il valore attuale è <code>{}</code>."
    SETTINGS_NOT_VALID_VALUE_FOR = "<code>{}</code> non è un valore valido per <code>{}</code>."
    SETTINGS_SET_TO = "<code>{}</code> impostato a <code>{}</code> (era <code>{}</code>)."
    SETTINGS_COULD_NOT_SET = "Impossibile impostare <code>{}</code> a <code>{}</code> (è <code>{}</code> ora)."
    MUST_BE_ADMIN = "Devi essere amminisatore per effettuare questa operazione."
    SETTINGS_HELP = """
<b>Comandi:</b>

<code>/settings</code>
Apri il menù delle impostazioni.

<code>/settings get</code>
Ricevi un file <code>json</code> con le impostazioni della chat corrente.

<code>/settings set &lt;item&gt; &lt;value&gt;</code>
Imposta <code>&lt;item&gt;</code> a <code>&lt;value&gt;</code>.

<b>Opzioni:</b>
- <code>lang</code> (lingua): la lingua che il bot userà per risponderti.
- <code>override</code> (sovrascrivi impostazioni gruppi, privata): se attiva, il bot ignora la lingua dei gruppi e usa la lingua impostata privatamente.
- <code>auto-tr</code> (auto translate, solo gruppi): se attiva, il bot traduce i messaggi inviati dagli utenti del gruppo, se necessario.
- <code>fwd</code> (inoltro chat): inoltra i messaggi di questa chat ai volontari di supporto, invece di usare il comando /hey ogni volta.
"""
    # encode
    ENCODE_FROM_TO = "Codifica {}da {} a {}"
    ENCODE_ERROR = "È avvenuto un errore. Assicurati che il testo fornito sia cofidicato correttamente."
    ENCODE_PROVIDED_ISNT = "La codifica del testo fornito non è <code>{}</code>."
    ENCODE_IS_NOT_VALID = "<code>{}</code> non è una codifica valida."
    ENCODE_ARE_NOT_VALID = "<code>{}</code> e <code>{}</code> non sono codifiche valide."
    PROVIDE_DECODING_ENCODING_TEXT = "Fornisci un formato di decodifica e codifica e del testo da analizzare."
    # translate
    TRANSLATION_TITLE = "Traduttore"
    SOURCE_TEXT = "Testo di origine"
    # QRCode
    QR_CODE_EMPTY = "Il contenuto era vuoto o OpenCV non l'ha captato."
    QR_CODE_NOT_FOUND = "Non sono stati individuati codici QR."
    QR_CODE_DETECTING = "Rilevando e decodificando il codice QR..."
    # score
    SCORE_HELP = """
<code>/score</code> - Gestisci gli score nella chat corrente.
Uno score è un insieme di elementi per i quali è registrato un numero intero ciascuno.

<b>Utilizzo:</b>

<code>/score new/create score_name</code>
Crea un nuovo score per la chat corrente.

<code>/score del/delete/remove score_name [other scores]</code>
Elimina uno (o più) score nella chat corrente.

<code>/score ren/rename score_name new_name</code>
Rinomina uno score. Questo non cambierà il suo nome in visualizzazione.

<code>/score display score_name display_name</code>
Imposta un nome in visualizzazione per uno score. Questo non rinominerà lo score.

<code>/score get/print score_name</code>
Visualizza lo score con i suoi elementi e relativi valori.

<code>/score set score_name item_name [value=1]</code>
Imposta un valore per l'elemento specificato.
L'elemento viene creato se non esiste e il valore è diverso da <code>0</code>.
Impostando il valore a <code>0</code> elimina l'elemento se esiste.

<code>/score add score_name item_name [value=1]</code>
Incrementa il valore di un elemento del valore specificato.
Se il nuovo valore è <code>0</code>, l'elemento viene conservato comunque.

<code>/score delitem score_name item_name</code>
Alias per <code>/score set score_name item_name 0</code>.

<pre>/score setraw score_name
item1 : value1
item2 : value2
item3:value3
item4 :value4
[...]</pre>
Sostituisce gli elementi di uno score esistente con quelli specificati.
Questo torna utile per copiare o unire score diversi, o per creare più elementi al volo in un nuovo score.
"""
    SCORE_HELP_ADD = "<code>/score add score_name item_name [value=1]</code>\n\nAumenta di <code>value</code> l'elemento <code>item_name</code> dello score <code>score_name</code>.\nSi possono usare valori negativi al posto di <code>value</code>."
    SCORE_HELP_SET = "<code>/score set score_name item_name [value=1]</code>\n\nImposta a <code>value</code> l'elemento <code>item_name</code> dello score <code>score_name</code>."
    SCORE_HELP_SETRAW = "<code>/score setraw score_name\nitem1 : value\nitem2 : value\nitem3 : value</code>\n\nPer ogni nuova riga, crea un elemento e vi assegna il valore specificato."
    SCORE_INVALID_NAME = "Nome score non valido: deve essere alfanumerico (trattini <code>-</code> e underscore <code>_</code> sono consentiti)."
    SCORE_PROVIDE_NAME = "Fornisci un nome valido per lo score."
    SCORE_PROVIDE_ITEM_NAME = "Fornisci un nome valido per l'elemento'."
    SCORE_DOESNT_EXIST = "Lo score <b>{}</b> non esiste."
    SCORE_CREATED_SUCCESSFULLY = "Lo score <b>{}</b> è stato creato con successo."
    SCORE_ALREADY_EXISTS = "Lo score <b>{}</b> è già esistente."
    SCORE_WAS_NOW_GONE = "Lo score era:\n\n{}\n\nOra è stato eliminato."
    SCORE_WAS = "Lo score era:\n\n{}"
    SCORE_NOW_ITS = "Ora è:\n\n{}"
    SCORE_RENAMED_FROM = "Lo score <b>{}</b> è stato rinominato in <b>{}</b>."
    SCORE_YOU_ARENT_AN_EDITOR = "Non sei un editor dello score."
    SCORE_YOU_ARENT_THE_OWNER = "Non sei il proprietario dello score."
    SCORE_ITEM_SET_TO = "<i>{}</i> di <b>{}</b> è stato impostato a <code>{}</code>."
    SCORE_NO_ITEMS = "Non ci sono elementi nello score, al momento."
    SCORE_ITEM_DOESNT_EXIST = "L'elemento <i>{}</i> non esiste in <b>{}</b>."
    SCORE_ITEM_DELETED = "L'elemento <i>{}</i> in <b>{}</b> è stato eliminato."
    SCORE_ONLY_NUMBERS = "Solo numeri interi sono consentiti come valori degli elementi."
    SCORE_DISPLAY_SET = "The score <b>{}</b> will now be displayed as <b>{}</b>."
    SCORE_UNNEEDED_ARGUMENT = "Argomenti non richiesti."
    # counter
    COUNTER_HELP = """
<code>/counter</code> - Gestisci i contatori nella chat corrente.
Un contatore registra un valore che può essere incrementato manualmente o autoamticamente quanto qualcuno scrive qualcosa.

<b>Usage:</b>

<code>/counter new/create counter_name</code>
Crea un nuovo contatore per la chat corrente.

<code>/counter del/delete/remove counter_name</code>
Elimina un contatore nella chat corrente.

<code>/counter ren/rename counter_name new_name</code>
Rinomina un counter. Questo non cambierà il suo nome in visualizzazione.

<code>/counter display counter_name display_name</code>
Imposta un nome in visualizzazione per il contatore. Questo non lo rinominerà.

<code>/counter get/print counter_name</code>
Visualizza il contatore e il suo valore.

<code>/counter set counter_name value</code>
Imposta un contatore ad un certo valore.

<code>/counter add counter_name [value=1]</code>
Aggiungi un certo valore ad un contatore.

<code>/counter auto add/del counter_name filter</code>
Aggiungi/elimina un filtro ad un contatore (modalità automatica).
Se un messaggio inviato contiene il filtro, il contatore sarà aggiornato.
"""
    COUNTER_IS = "<b>{}</b> è impostato a <code>{}</code>."
    COUNTER_SET = "<b>{}</b> impostato a <code>{}</code>."
    COUNTER_ALREADY_EXISTS = "Il contatore è già esistente."
    COUNTER_COULDNT_CREATE = "Impossibile creare il contatore."
    COUNTER_CREATED = "Contatore creato."
    COUNTER_YOU_ARENT_THE_OWNER = "Non sei il proprietario del contatore."
    COUNTER_YOU_ARENT_AN_EDITOR = "Non sei un editor del contatore."
    COUNTER_DOESNT_EXIST = "<b>{}</b> non esiste."
    COUNTER_DELETED = "<b>{}</b> è stato eliminato (il suo valore era <code>{}</code>)."
    COUNTER_RENAMED_FROM = "<b>{}</b> è stato rinominato in <b>{}</b>."
    COUNTER_DISPLAY_SET = "<b>{}</b> sarà visualizzato come <b>{}</b>."
    COUNTER_AUTO_HAS = "<b>{}</b> ora ha i seguenti filtri:\n<i>{}</i>"
    COUNTER_WORD_NOT_FOUND = "<i>{}</i> non è tra i filtri:\n<i>{}</i>"
    COUNTER_PROVIDE_NAME = "Fornisci un valore valido per il contatore.\nSolo lettere, cifre, trattini e underscore (<code>-</code> e <code>_</code>) sono ammessi."
    COUNTER_NO_TRIGGERS = "Nessun filtro impostato."
    COUNTER_ONLY_NUMBERS = "Si può solo impostare numeri."
    # Other commands
    SHUFFLE_TEXT = "Scombina il testo"
    ################
    #   COMMANDS   #
    ################
    COMMANDS = {
        "help": "Info sul comando <code>command</code>.\nOmetti <code>command</code> per ottenere una lista di comandi disponibili.",
        "settings": "Cambia le preferenze per la chat corrente.\n<code>/settings get</code> per ricevere un file json contenente le impostazioni (eventuale debugging).\n<code>/settings set &lt;item&gt; &lt;value&gt;</code> per cambiare una specifica opzione velocemente.",
        "translate": 'Traduci <code>text</code> da <code>from_lang</code> a <code>to_lang</code>.\n<code>from_lang</code> e <code>to_lang</code> devono essere "auto" o un identificatore di lingua valido (come <i>en</i>, <i>it</i>, <i>de</i>...).\nUsando l\'alias <code>/tr</code>, il risultato sarà mostrato direttamente senza dettagli.\n<code>text</code> può essere omesso se si risponde ad un messaggio.',
        "tts": "Text to speech, rendi <code>text</code> del testo parlato e ricevi un file <code>mp3</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
        "qr": "Crea un codice QR da <code>text</code>.\nPer decodificare un codice QR, rispondere ad una foto che lo contiene omettendo <code>text</code>.",
        "wordfor": "Ottieni la parola che definisce <code>definition</code>, attraverso Reverse Dictionary (solo inglese).",
        "encode": "Codifica del testo da <code>x</code> a <code>y</code>.\nValori accetti per x e y:\n- text, txt, t\n- binary, bin, b\n- base64, b64\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
        "pokemon": "Ottieni dati su <code>name</code> della categoria <code>category</code>.\nPuoi cercare direttamente un elemento senza specificare una categoria (per esempio <code>/pokemon ditto</code> equivale a <code>/pokemon pokemon ditto</code>).\nInviare <code>/pokemon</code> per ottenere una lista di categorie disponibili dal bot.",
        "score": "Crea e gestisci gli score nella chat corrente. <code>/score help</code> per ulteriori dettagli.",
        "counter": "Crea e gestisci i contatori nella chat corrente. <code>/counter help</code> per ulteriori dettagli.",
        "random": "Genera un numero casuale da <code>x</code> (0 come predefinito) a <code>y</code> (100 come predefinito).",
        "pickrandom": "Rispondendo ad un messaggio scritto su più righe con questo comando, una o più righe (<code>limit</code> come limite, 1 come predefinito) saranno prese e mostrate a caso.",
        "shuffle": "Scombina <code>text</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
        "imdumb": "Rendi <code>text</code> scritto come se fossi stupido. <code>text</code> può essere omesso se si risponde ad un messaggio.",
        "say": "Fa' dire <code>text</code> al bot.",
        "len": "Visualizza la lunghezza di <code>text</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
    }
    QUERY_COMMANDS = {
        "translate": """Traduci "text" da "from_lang" a "to_lang".""",
        "imdumb": """Scrivi messaggi come se fossi stupido.""",
        "encode": """Converti "text" dalla codifica "x" alla codifica "y".""",
        "pokemon": """Cerca "name" nella categoria "category" su PokeAPI.""",
        "wordfor": """Ottieni la parola per "definition" attraverso Reverse Dictionary (solo inglese).""",
    }
    QUERY = {
        "help": {
            "title": "Aiuto riguardo i comandi",
            "content": "Per ottenere aiuto, avviare il bot in privato e inviare /help.",
            "description": "Avviare il bot in privato per ottenere aiuto.",
        },
    }
