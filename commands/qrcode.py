from bot.classes import BaseCommand

import base64
import cv2
import io
import os
import pyqrcode
import tempfile
import uuid


class CmdQRCode(BaseCommand):
    name = "qr"
    args = ["[text]"]

    def function(self, text) -> bytes:  # Get qrcode from string
        return io.BytesIO(
            base64.b64decode(
                pyqrcode.create(text, encoding="utf-8").png_as_base64_str(scale=6)
            )
        )

    async def run(self, bot, m):
        if m.reply_to_message is not None and m.reply_to_message.photo:
            file_path = f"{tempfile.gettempdir()}/qrcode{uuid.uuid4()}.png"
            r = await m.reply_text(m.lang.DOWNLOADING)
            await m.reply_to_message.download(file_path)
            await r.edit(m.lang.QR_CODE_DETECTING)
            data, bbox, straight_qrcode = cv2.QRCodeDetector().detectAndDecode(
                cv2.imread(file_path)
            )
            if bbox is not None:
                await r.edit(data or m.lang.QR_CODE_EMPTY)
            else:
                await r.edit(m.lang.QR_CODE_NOT_FOUND)
            os.remove(file_path)
        else:
            file_path = f"{tempfile.gettempdir()}/qrcode{uuid.uuid4()}.png"
            pyqrcode.create(
                " ".join((m.text or m.caption).split(" ")[1:]), encoding="utf-8"
            ).png(file_path, scale=6)
            with open(file_path, "rb") as f:
                await m.reply_photo(photo=f)
            os.remove(file_path)
