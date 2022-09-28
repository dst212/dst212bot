name = "Italiano"
flag = "🇮🇹"
strings = {
"YES": "Sì",
"NO": "No",
"IM_SMORT": "SoNo InTeLlIgEnTe!!!!!!",

# specific messages
"WELCOME_MESSAGE": "Benvenutə, {}.\nPer vedere i comandi disponibili, invia /help.\nPer personalizzare le tue preferenze, invia /settings.",
"HI_THERE_ADMIN": "Ehilà {}, al tuo servizio.",
"HI_THERE_USER": "Ehilà {}, puoi avviarmi in privato, ti aspetterò lì :)",
"LETS_START": "Iniziamo!",
"CREDITS_MESSAGE": f"""
<b>Crediti</b>

Bot scritto in Python da @dst212.
https://dst212.github.io/

<b>Librerie</b>
- <code>pyrogram</code>: client Telegram
- <code>opencv-python</code>: rilevamento e lettura codici QR
- <code>pyqrcode</code>: generazione codici QR
- <code>googletrans</code> (3.1.0a0): API per il traduttore
- <code>gtts</code>: API per il text-to-speech

<b>Risorse dati</b>
- <i>Reverse Dictionary</i>: https://reversedictionary.org
- <i>Pokémon</i>: https://pokeapi.co/
- <i>Pokémon GO</i>: https://pokemondb.net/
""",

# generic words and placeholders
"ERROR": "Errore",
"EXAMPLE": "Esempio",
"ALIASES": "Alias",
"RESULTS": "Risultati",
"USAGE": "Utilizzo",
"SYNTAX": "Sintassi",
"HELP": "Aiuto",
"BACK": "Indietro",
"CLOSE": "Chiudi",
"UNKNOWN": "Sconosciuto",
"AVAILABLE_CATEGORIES": "Categorie disponibili",

# titles
"TRANSLATION_TITLE": "Traduttore",

# notices
"INLINE_MODE_NOTICE": "Nella modalità inline, scrivere i comandi senza la slash <code>/</code> e inserire sempre il testo di input.",
"CHOOSE_A_BUTTON": "Premere un pulsante per avere informazioni su quel comando.",
"DOWNLOADING": "Scaricamento...",
"LOADING": "Caricamento...",
"RESTARTING_BOT": "Riavviando il bot...",
"FETCHING_DATA": "Recupero dati...",
"CLICK_HERE_TO_BE_RETARDED": "Clicca qui per essere ritardato",

# generic warnings
"LOL_NO_THANKS": "Lol no grazie.",
"WE_ALL_KNOW_THAT": "Lo sappiamo tutti.",
"AN_ERROR_OCCURRED": "È avvenuto un errore.",
"ERROR_OCCURRED": "È avvenuto un errore.",
"AN_ERROR_OCCURRED_WHILE_PERFORMING": "È avvenuto un errore durante l'esecuzione di questa operazione.\nContatta @dst212 per ulteriori informazioni.",
"NO_RESULTS": "Nessun risultato.",
"NO_RESULTS_FOR": "Nessun risultato per {}.",
"DOESNT_EXIST": "{} non esiste.",
"INVALID_SYNTAX": "Sintassi invalida.",
"INVALID_USAGE": "Utilizzo invalido.",
"PROVIDE_TEXT": "Fornire del testo rispondendo ad un messaggio o scrivendolo accanto al comando.",
"PROVIDE_SEARCH_QUERY": "Fornire una stringa di ricerca.",
"COULDNT_FIND_SECTION": "Impossibile trovare la sezione {}.",
"ERROR_WHILE_CREATING_FILE": "Errore nella creazione del file.",
"NOT_AVAILABLE_AT_THIS_TIME": "Non disponibile al momento.",
"IS_NOT_AVAILABLE_AT_THIS_TIME": "{} non è al momento disponibile.",
"PICK_RANDOM_REPLY_TO_A_MESSAGE": "Per usare questo comando, Rispondere ad un messaggio con più di una riga.\nIl bot ne sceglierà una (o più).\n<code>/help pickrandom</code> per ulteriori informazioni.",
"IS_INVALID_USING": "<code>{}</code> non è un valore valido, verrà usato <code>{}</code>.",
"NO_ENTRY_FOR": "Nessuna voce per {}.",
"NO_PERMISSIONS": "Non hai i permessi per effettuare questa operazione.",
"LANGUAGE_IS_NOT_SUPPORTED": "La lingua <code>{}</code> non è supportata.",
"USING_LANGUAGE": "Verrà usata la lingua <code>{}</code>.",

"INVALID_COMMAND": "<code>{}</code> non è un comando valido.",
"UNNEEDED_ARGUMENT": "Ci sono argomenti non necessari.",
"WEBSITE_UNAVAILABLE": "Sito non disponibile.",
"PROVIDE_DECODING_ENCODING_TEXT": "Fornire un formato di decodifica e codifica e del testo da analizzare.",
"PROVIDE_USERNAME_OR_ID": "Fornire un username o un id valido.",
"YOU_SHOULD_KNOW": "Dovresti saperlo...",

# generic info
"RESULTS_FOR": "Risultati per {}",
"ENCODE_FROM_TO": "Codifica {}da {} a {}",
"TRANSLATE_FROM_TO": "Traduci {}da {} a {}",
"FILE_SAVED": "Salvato {}.",
"CATEGORY_DOESNT_EXIST": "La categoria specificata non esiste.",
"IT_DOESNT_EXIST": "La categoria {} non esiste.",
"DID_YOU_MEAN": "Intendevi {}?",

# settings
"SETTINGS_FOR_THIS_CHAT": "Qui si può cambiare le impostazioni per questa chat.",
"SETTINGS_OVERRIDE": "Sovrascrivi impostazioni gruppi",
"SETTINGS_AUTO-TR": "Auto-traduci i messaggi",
"SETTINGS_SYNC-TR": "Sincronizza lingua con /translate",
"SETTINGS_SELECT_VALUE": "Scegli un nuovo valore per <code>{}</code>. Il valore attuale è <code>{}</code>.",
"MUST_BE_ADMIN": "Devi essere amminisatore per effettuare questa operazione.",

# QRCode
"QR_CODE_EMPTY": "Il contenuto era vuoto o OpenCV non l'ha captato.",
"QR_CODE_NOT_FOUND": "Non sono stati individuati codici QR.",
"QR_CODE_DETECTING": "Rilevando e decodificando il codice QR...",

# info
"INFO_FOR": "Info su",
"INFO_FOR_TITLE": "<i>Info su <u>{}</u></i>",
"INFO_USERNAME": "<b>Username</b>: @{}",
"INFO_MENTION": "<b>Mention</b>: {}",
"INFO_MEMBERS": "<b>Membri</b>: {}",
"INFO_ID": "<b>ID</b>: <code>{}</code>",
"INFO_DC": "<b>DC</b>: {}",
"INFO_PHONE": "<b>Numero di telefono</b>: {}",
"INFO_STATUS": "<b>Stato</b>: ",
"INFO_STATUS_ONLINE": "online",
"INFO_STATUS_OFFLINE": "offline",
"INFO_STATUS_RECENTLY": "ultimo accesso di recente",
"INFO_STATUS_LAST_WEEK": "ultimo accesso in una settimana",
"INFO_STATUS_LAST_MONTH": "ultimo accesso in un mese",
"INFO_STATUS_LONG_AGO": "ultimo accesso tanto tempo fa",
"INFO_LANGUAGE_CODE": "<b>Codice lingua</b>: {}",
"INFO_THIS_USER_IS": "Questo utente è {}",
"INFO_THIS_CHAT_IS": "Questo gruppo è {}",
"INFO_VERIFIED": "verificato",
"INFO_DELETED": "eliminato",
"INFO_BOT": "a bot",
"INFO_RESTRICTED": "ristretto",
"INFO_SCAM": "segnato come scam",
"INFO_FAKE": "falso",
"INFO_SUPPORT": "di supporto",
"INFO_PROTECTED": "Questo gruppo ha i contenuti protetti.",
"INFO_ME": "Aspetta... sono io?",

# score
"SCORE_HELP": f"""
<code>/score</code> - Gestisci gli score nella chat corrente.
Uno score è un insieme di elementi per i quali è registrato un numero intero.

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
""",
"SCORE_INVALID_NAME": "Nome score non valido: deve essere alfanumerico (trattini <code>-</code> e underscore <code>_</code> sono consentiti).",
"SCORE_PROVIDE_NAME": "Fornire un nome valido per lo score.",
"SCORE_PROVIDE_ITEM_NAME": "Fornire un nome valido per l'elemento'.",
"SCORE_DOESNT_EXIST": "Lo score <b>{}</b> non esiste.",
"SCORE_CREATED_SUCCESSFULLY": "Lo score <b>{}</b> è stato creato con successo.",
"SCORE_ALREADY_EXISTS": "Lo score <b>{}</b> è già esistente.",
"SCORE_WAS_NOW_GONE": "Lo score era:\n\n{}\n\nOra è stato eliminato.",
"SCORE_WAS": "Lo score era:\n\n{}",
"SCORE_NOW_ITS": "Ora è:\n\n{}",
"SCORE_RENAMED_FROM": "Lo score <b>{}</b> è stato rinominato in <b>{}</b>.",
"SCORE_YOU_ARENT_AN_EDITOR": "Non sei un editor dello score.",
"SCORE_YOU_ARENT_THE_OWNER": "Non sei il proprietario dello score.",
"SCORE_ITEM_SET_TO": "<i>{}</i> di <b>{}</b> è stato impostato a <code>{}</code>.",
"SCORE_NO_ITEMS": "Non ci sono elementi nello score, al momento.",
"SCORE_ITEM_DOESNT_EXIST": "L'elemento <i>{}</i> non esiste in <b>{}</b>.",
"SCORE_ITEM_DELETED": "L'elemento <i>{}</i> in <b>{}</b> è stato eliminato.",
"SCORE_ONLY_NUMBERS": "Solo numeri interi sono consentiti come valori degli elementi.",
"SCORE_DISPLAY_SET": "The score <b>{}</b> will now be displayed as <b>{}</b>.",
"SCORE_UNNEEDED_ARGUMENT": "Argomenti non richiesti.",

# counter
"COUNTER_HELP": f"""
<code>/counter</code> - Gestisci i contatori nella chat corrente.
Un contatore mantiene un valore che può essere incrementato manualmente o autoamticamente quanto qualcuno scrive qualcosa.

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
""",
"COUNTER_IS": "<b>{}</b> è impostato a <code>{}</code>.",
"COUNTER_SET": "<b>{}</b> impostato a <code>{}</code>.",
"COUNTER_ALREADY_EXISTS": "Il contatore è già esistente.",
"COUNTER_COULDNT_CREATE": "Impossibile creare il contatore.",
"COUNTER_CREATED": "contatore creato.",
"COUNTER_YOU_ARENT_THE_OWNER": "Non sei il proprietario del contatore.",
"COUNTER_YOU_ARENT_AN_EDITOR": "Non sei un editor del contatore.",
"COUNTER_DOESNT_EXIST": "<b>{}</b> non esiste.",
"COUNTER_DELETED": "<b>{}</b> è stato eliminato (il suo valore era <code>{}</code>).",
"COUNTER_RENAMED_FROM": "<b>{}</b> è stato rinominato in <b>{}</b>.",
"COUNTER_DISPLAY_SET": "<b>{}</b> sarà visualizzato come <b>{}</b>.",
"COUNTER_AUTO_HAS": "<b>{}</b> ora ha i seguenti filtri:\n<i>{}</i>",
"COUNTER_WORD_NOT_FOUND": "<i>{}</i> non è tra i filtri:\n<i>{}</i>",
"COUNTER_PROVIDE_NAME": "Fornire un valore valido per il contatore.\nSolo lettere, cifre, trattini e underscore (<code>-</code> e <code>_</code>) sono ammessi.",
"COUNTER_NO_TRIGGERS": "Nessun filtro impostato.",
"COUNTER_ONLY_NUMBERS": "Si può solo impostare numeri.",

# pokemon go
"POGO_HELP": """
<code>/pogo</code> - Ricevi info riguardo il rank dato il numero del rank o la configurazione IV.

<b>Utilizzo:</b>
<code>/pogo &lt;pokémon name&gt; &lt;rank number/IVs&gt; [keywords]</code>
o
<code>/pogo &lt;pokémon name&gt; &lt;rank number/IVs&gt; &lt;CPs cap&gt; &lt;minimum IVs&gt; &lt;level cap&gt;</code>

<b>Parole chiave che cambiano il limite dei PL:</b> <i>(il valore predefinito è <code>1500</code>)</i>
- Qualsiasi nome di una lega: <code>great</code>, <code>ultra</code>, <code>master</code>, <code>little</code>
- Alias dei nomi delle leghe: <code>gl</code>, <code>ul</code>, <code>ml</code>, <code>lc</code> or <code>ll</code>
- Coppe classiche (che impostano anche il massimo livello a 40): <code>glpc</code> and <code>glc</code> (which actually don't exist), <code>ulpc</code> and <code>ulc</code>, <code>mlpc</code> and <code>mlc</code>

<b>Parole chiave che cambiano gli IV minimi:</b> <i>(il valore predefinito è <code>0</code>)</i>
- Minimo <code>12</code> di IV: <code>lucky</code>
- Minimo <code>10</code> di IV: <code>raid</code>, <code>egg</code>, <code>reward</code>, <code>mythical</code>
- Minimo <code>5</code> di IV: <code>best friend</code>
- Minimo <code>4</code> di IV: <code>weather boosted</code>, <code>weather boost</code>, <code>weather</code>
- Minimo <code>3</code> di IV: <code>ultra friend</code>
- Minimo <code>2</code> di IV: <code>great friend</code>
- Minimo <code>1</code> di IV: <code>good friend</code>
- Minimo <code>0</code> di IV: <code>wild</code>

<b>Parole chiave che influenzano il limite del livello:</b> <i>(il valore predefinito è <code>50</code>)</i>
- A seconda della lega specificata in precedenza, classica o normale, il limite sarà impostato rispettivamente a 41 o 51: <code>bb</code>, <code>best buddy</code>

<b>Esempi:</b>
<code>/pogo umbreon</code>
Info sul rank 1 di Umbreon's nella Lega Mega.

<code>/pogo medicham 1 bb</code>
Info sul rank 1 di Medicham nella Lega Mega con livello massimo 51.

<code>/pogo talonflame 15/15/14 ultra</code>
Info sul rank di Talonflame con quegli IV (attacco/difesa/stamina) nella Lega Ultra. 
Gives info about Talonflame's rank with those IVs (attack/defense/stamina) in Ultra League.

<code>/pogo registeel 1 raid</code>
Info sul rank 1 di Registeel con IV da Raid nella Lega Mega.

<code>/pogo nidoqueen 15/15/15 ulc</code>
Info sul rank di Nidoqueen con quegli IV in Lega Ultra Classica.

Nella modalità inline, i comandi sono uguali:
 <code>@dst212bot pogo umbreon</code>
è la stessa cosa di:
 <code>/pogo umbreon</code>

Il PokéDex fa riferimento ai dati su <a href="https://pokemondb.net/go/pokedex">PokemonDB</a>.
""",
"POGO_INVALID_USAGE": "Utilizzo non valido.\nInviare <code>/pogo help</code> per ottenere dettagli sull'utilizzo.",
"POGO_IV_MUST_BE_BETWEEN": "Dati non validi: gli IV devono essere 3 numeri interi tra <code>0</code> e <code>15</code>.",
"POGO_RANK_MUST_BE_BETWEEN": "Dati non validi: il rank dev'essere un numero intero tra <code>1</code> e <code>{}</code>.",
"POGO_ENSURE_DATA_IS_CORRECT": "Dati non validi: assicurarsi che tutto sia corretto. Inviare <code>/pogo help</code> per ottenere dettagli sull'utilizzo.",
"POGO_MAX_CP_LT_10": "I PL massimi non possono essere inferiori a <code>10</code>.",
"POGO_MAX_LVL_LT_0": "Il livello massimo non può esser meno di <code>0</code>.",
"POGO_MIN_IV_MT_15": "Gli IV minimi non possono essere maggiori di <code>15</code>.",
"POGO_NOT_RECOGNIZED": "<code>{}</code> non è riconosciuta come parola chiave.",

# Other commands
"SCRAMBLE_TEXT": "Scombina il testo",

################
### COMMANDS ###
################

"COMMANDS": {
	"help": "Info su <code>command</code>.\nOmettere <code>command</code> per ottenere una lista di comandi disponibili.",
	"settings": "Cambia le preferenze per la chat corrente.\nInvia <code>/settings get</code> per ottenere un file json contenente le impostazioni (eventuale debugging). Non c'è alcun modo per effettuare l'opposto (si deve cambiare le impostazioni manualmente, <s><code>/settings set</code></s> non esiste).",
	"translate": "Traduci <code>text</code> da <code>from_lang</code> a <code>to_lang</code>.\n<code>from_lang</code> e <code>to_lang</code> devono essere \"auto\" o un identificatore di lingua valido (come <i>en</i>, <i>it</i>, <i>de</i>...).\nUsando l'alias <code>/tr</code>, il risultato sarà mostrato direttamente senza dettagli.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
	"tts": "Text to speech, rendi <code>text</code> del testo parlato e ottieni un file <code>mp3</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
	"qr": "Crea un codice QR da <code>text</code>.\nPer decodificare un codice QR, rispondere ad una foto che lo contiene omettendo <code>text</code>.",
	"wordfor": "Ottieni la parola che definisce <code>definition</code>, attraverso Reverse Dictionary (solo inglese).",
	"encode": "Codifica del testo da <code>x</code> a <code>y</code>.\nValori accetti per x e y:\n- text, txt, t\n- binary, bin, b\n- base64, b64\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
	"pokemon": "Ottieni dati su <code>name</code> della categoria <code>category</code>.\nPuoi cercare direttamente un elemento senza specificare una categoria (per esempio <code>/pokemon ditto</code> equivale a <code>/pokemon pokemon ditto</code>).\nInviare <code>/pokemon</code> per ottenere una lista di categorie disponibili dal bot.",
	"pogo": "Ottieni dati su roba di Pokémon GO. <code>/pogo help</code> per ulteriori dettagli.",
	"score": "Crea e gestisci gli score nella chat corrente. <code>/score help</code> per ulteriori dettagli.",
	"counter": "Crea e gestisci i contatori nella chat corrente. <code>/counter help</code> per ulteriori dettagli.",
	"random": "Genera un numero casuale da <code>x</code> (0 come predefinito) a <code>y</code> (100 come predefinito).",
	"pickrandom": "Rispondendo ad un messaggio scritto su più righe con questo comando, una o più righe (<code>limit</code> come limite, 1 come predefinito) saranno prese e mostrate a caso.",
	"scramble": "Scombina <code>text</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
	"imdumb": "Rendi <code>text</code> scritto come se fossi stupido. <code>text</code> può essere omesso se si risponde ad un messaggio.",
	"say": "Fa' dire <code>text</code> al bot.",
	"len": "Visualizza la lunghezza di <code>text</code>.\n<code>text</code> può essere omesso se si risponde ad un messaggio.",
	"count": "Conta i messaggi in una chat.\nSe si risponde ad un messaggio, il conteggio parte da lì.",
	"info": "Ottieni info su un utente rispondendo ad un messaggio.\nSe non si risponde ad un messaggio e <code>username</code> e <code>id</code> vengono omessi, si ottengono info sulla chat corrente.",
	"repeat": "Fa' analizzare un messaggio nuovamente al bot rispondendovi.",
	"hey": "Contatta un amministratore del bot.",
},
"QUERY_COMMANDS": {
	"translate": """Traduci "text" da "from_lang" a "to_lang".""",
	"info": """Ottieni info su un utente/canale/gruppo su Telegram.""",
	"imdumb": """Scrivi messaggi come se fossi stupido.""",
	"encode": """Converte "text" dalla codifica "x" alla codifica "y".""",
	"pokemon": """Cerca "name" nella categoria "category" su PokeAPI.""",
	"wordfor": """Ottieni la parola per "definition" attraverso Reverse Dictionary (solo inglese).""",
},
"QUERY": {
	"help": {
		"title": "Aiuto riguardo i comandi",
		"content": "Per ottenere aiuto, avviare il bot in privato e inviare /help.",
		"description": "Avviare il bot in privato per ottenere aiuto."
	},
},
}
