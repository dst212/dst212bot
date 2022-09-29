from bot.classes import Command
import html, os
from googletrans import Translator
from gtts import gTTS
from hashlib import md5

class CmdTTS(Command):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = "tts"
		self.args = ["[text]"]
		self.base_dir = "data/cache/audio/"

		self.translator = Translator()

	def run(self, LANG, bot, m) -> None:
		os.makedirs(self.base_dir, exist_ok=True)
		m_text = m.text or m.caption
		text = ""
		lang = ""
		#get text to turn into speech
		i = m_text.find(" ")
		if i != -1:
			text = m_text[i+1:]
		else:
			i = len(m_text)
		if not text:
			if m.reply_to_message:
				text = m.reply_to_message.text or m.reply_to_message.caption
			else:
				m.reply_text(LANG('PROVIDE_TEXT'))
				return
		#start doing stuff
		msg = m.reply_text("Processing...")
		j = m_text[:i].find("-")
		lang = m_text[j+1:i] if j != -1 else translator.detect(text).lang
		if type(lang) == list:
			lang = lang[0]
		filepath = f"{self.base_dir}{md5(text.encode()).hexdigest()}.{lang}.mp3"
		#save the speech to a file
		if not os.path.exists(filepath):
			msg.edit_text(f"Creating...")
			try:
				gTTS(text, lang=lang).save(filepath)
			except:
				if j == -1:
					newlang = "en"
					msg.edit_text(LANG('LANGUAGE_IS_NOT_SUPPORTED').format(html.escape(lang)) + "\n" + LANG('USING_LANGUAGE').format(newlang))
					filepath = filepath[:-len(f".{lang}.mp3")] + f".{newlang}.mp3"
					lang = newlang
					gTTS(text, lang=lang).save(filepath)
				else:
					msg.edit_text(LANG('ERROR_WHILE_CREATING_FILE'))# + f"\n{lang}, {text}, {i}, {j}")
					return
		msg.edit_text("Uploading...")
		with open(filepath, "rb") as f:
			bot.send_audio(msg.chat.id, f, file_name=f"text-to-speech.{lang}.mp3", caption="Audio for text:\n<code>" + html.escape(text[:1000]) + "</code>")
		msg.delete()

	#TODO inlinequery