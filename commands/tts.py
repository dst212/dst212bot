import html, os
from googletrans import Translator
from gtts import gTTS
from hashlib import md5

translator = Translator()
BASE_DIR = "data/audio/"

def command(LANG, bot, message) -> None:
	os.makedirs(BASE_DIR, exist_ok=True)
	m_text = message.text or message.caption
	text = ""
	lang = ""
	#get text to turn into speech
	i = m_text.find(" ")
	if i != -1:
		text = m_text[i+1:]
	else:
		i = len(m_text)
	if not text:
		if message.reply_to_message:
			text = message.reply_to_message.text or message.reply_to_message.caption
		else:
			message.reply_text(LANG('PROVIDE_TEXT'))
			return
	#start doing stuff
	msg = message.reply_text("Processing...")
	j = m_text[:i].find("-")
	lang = m_text[j+1:i] if j != -1 else translator.detect(text).lang
	filepath = BASE_DIR + lang + md5(text.encode()).hexdigest() + ".mp3"
	#save the speech to a file
	if not os.path.exists(filepath):
		msg.edit_text(f"Creating...")
		try:
			gTTS(text, lang=lang).save(filepath)
		except:
			if j == -1:
				msg.edit_text(LANG('LANGUAGE_IS_NOT_SUPPORTED').format(html.escape(lang)) + "\n" + LANG('USING_LANGUAGE').format('en'))
				gTTS(text, lang="en").save(filepath)
			else:
				msg.edit_text(LANG('ERROR_WHILE_CREATING_FILE'))# + f"\n{lang}, {text}, {i}, {j}")
				return
	msg.edit_text("Uploading...")
	bot.send_audio(msg.chat.id, open(filepath, "rb"), file_name="text-to-speech.mp3", caption="Audio for text:\n<code>" + html.escape(text[:1000]) + "</code>")
	msg.delete()

#TODO inlinequery