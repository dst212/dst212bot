import logging, base64, cv2, uuid, os, io, tempfile
import pyqrcode

class QRCode:
	def __init__(self, users):
		self.__usr = users

	def function(self, text) -> bytes: #get qrcode from string
		return io.BytesIO(base64.b64decode(pyqrcode.create(text, encoding="utf-8").png_as_base64_str(scale=6)))

	def command(self, LANG, bot, message) -> None:
		if message.reply_to_message is not None and message.reply_to_message.photo:
			file_path = tempfile.gettempdir() + "/qrcode" + str(uuid.uuid4()) + ".png"
		# try:
			msg = message.reply_text(LANG('DOWNLOADING'))
			message.reply_to_message.download(file_path)
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
			pyqrcode.create(" ".join((message.text or message.caption).split(" ")[1:]), encoding="utf-8").png(file_path, scale=6)
			with open(file_path, "rb") as f:
				message.reply_photo(photo=f)
			os.remove(file_path)
