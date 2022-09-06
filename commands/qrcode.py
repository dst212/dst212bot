from bot.classes import Command
import logging, base64, cv2, uuid, os, io, tempfile
import pyqrcode

class CmdQRCode(Command):
	def function(self, text) -> bytes: #get qrcode from string
		return io.BytesIO(base64.b64decode(pyqrcode.create(text, encoding="utf-8").png_as_base64_str(scale=6)))

	def run(self, LANG, bot, m):
		if m.reply_to_message is not None and m.reply_to_message.photo:
			file_path = tempfile.gettempdir() + "/qrcode" + str(uuid.uuid4()) + ".png"
		# try:
			msg = m.reply_text(LANG('DOWNLOADING'))
			m.reply_to_message.download(file_path)
			msg.edit_text(LANG('QR_CODE_DETECTING'))
			data, bbox, straight_qrcode = cv2.QRCodeDetector().detectAndDecode(cv2.imread(file_path))
			if bbox is not None:
				msg.edit_text(data or LANG('QR_CODE_EMPTY'))
			else:
				msg.edit_text(LANG('QR_CODE_NOT_FOUND'))
		# except:
		# 	msg.edit_text(LANG('ERROR_OCCURRED'))
		# finally:
			os.remove(file_path)
		else:
			file_path = tempfile.gettempdir() + "/qrcode" + str(uuid.uuid4()) + ".png"
			pyqrcode.create(" ".join((m.text or m.caption).split(" ")[1:]), encoding="utf-8").png(file_path, scale=6)
			with open(file_path, "rb") as f:
				m.reply_photo(photo=f)
			os.remove(file_path)
