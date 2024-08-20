from json import dumps
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from urllib.parse import urlparse, parse_qs
import sys, qrcode, requests, asyncio, websockets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath

# url parsing
def get_query_string(url):
    response_url = urlparse(url)
    query_string = response_url.query
    parse_string = parse_qs(query_string)

    return parse_string

# qr
url = {base_url/exercise/qr}
response = requests.get(url)
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_L,
    box_size = 8,
    border = 4,
)
qr.add_data(response.text)
qr.make(fit = True)

img = qr.make_image(fill_color="black", back_color="white")
img.save({png})

# sessionId
parsingData = get_query_string(response.text)
print(parsingData)

sessionId = parsingData['sessionId'][0]

async def connect():
    global sessionId
    uri = {base_url/exercise}
    async with websockets.connect(uri) as websocket:
        data = {
            "messageType": "ENTER",
            "sessionId": sessionId,
            "senderId": "13b1549f-42aa-4ff8-9955-d710c426c6c3"
        }
        await websocket.send(dumps(data))
        websocket_response = await websocket.recv()
        print(websocket_response)

        # 연결 유지
        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed")
                break


def round_image(self, pixmap, radius):
    size = pixmap.size()

    rounded = QPixmap(size)
    rounded.fill(Qt.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(pixmap))
    painter.setPen(Qt.NoPen)

    path = QPainterPath()
    path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)
    painter.drawPath(path)

    painter.end()
    return rounded

class QR_Page(QMainWindow):
    def __init__(self):
        super().__init__()
        super(QR_Page, self).__init__()

        loadUi("QR_Page_UI.ui", self)
        self.setWindowTitle("QR")

        self.imageLabel.setStyleSheet(
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: #E4E4E4;"
            "border-radius: 30px;")

        pixmap = QPixmap("QR.png").scaled(370, 370)
        rounded_pixmap = round_image(self, pixmap, 40)
        self.imageLabel.setPixmap(rounded_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QR_Page()
    mainWindow.show()
    asyncio.get_event_loop().run_until_complete(connect())
    sys.exit(app.exec_())