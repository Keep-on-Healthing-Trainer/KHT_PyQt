import sys, qrcode, requests, json
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import uic
from urllib.parse import urlparse, parse_qs
import websockets
import asyncio
from Timer_Page import Timer

def get_query_string(url):
    print(f"Parsing query string : {url}", flush=True)
    response_url = urlparse(url)
    query_string = response_url.query
    parse_string = parse_qs(query_string)
    print(f"Parsed query string: {parse_string}", flush=True)
    return parse_string

class WebSocketThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, sessionId):
        super().__init__()
        self.sessionId = sessionId

    def run(self):
        asyncio.run(self.connect_to_server())

    async def connect_to_server(self):
        uri = {wss://uri/exercise}
        print(f"Connecting to WebSocket: {uri}", flush=True)
        try:
            async with websockets.connect(uri) as websocket:
                data = {
                    "messageType": "ENTER",
                    "sessionId": self.sessionId,
                    "senderId": "13b1549f-42aa-4ff8-9955-d710c426c6c3"
                }
                await websocket.send(json.dumps(data))
                print(f"Send data to websocket: {data}", flush=True)

                websocket_response = await websocket.recv()
                print(f"WebSocket server response: {websocket_response}", flush=True)

                while True:
                    try:
                        message = await websocket.recv()
                        print(f"Received message from WebSocket: {message}", flush=True)
                        self.message_received.emit(message)

                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket connection closed", flush=True)
                        break
        except Exception as e:
            print(f"WebSocket connection error: {e}", flush=True)

class QR_Page(QDialog):
    def __init__(self, exType, widget):
        super().__init__()
        print("load QR_Page_UI", flush=True)

        self.widget = widget
        try:
            uic.loadUi("QR_Page_UI(1).ui", self)
            print("Successfully loaded QR_Page_UI", flush=True)
        except Exception as e:
            print(f"Failed to load QR_Page_UI: {e}", flush=True)
            return

        self.setWindowTitle("QR")
        self.exType = exType
        print(f"Exercise Type: {self.exType}", flush=True)

        self.imageLabel.setStyleSheet(
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: #E4E4E4;"
            "border-radius: 30px;"
        )

        self.sessionId = self.get_session_id()
        print(f"Session ID received: {self.sessionId}", flush=True)

        self.websocket_thread = WebSocketThread(self.sessionId)
        self.websocket_thread.message_received.connect(self.handle_websocket_message)
        self.websocket_thread.start()

    def get_session_id(self):
        print("get session ID", flush=True)
        url = {https://url/exercise/qr}
        try:
            response = requests.get(url)
            print(f"Server response: {response.text}", flush=True)

            qr_img = qrcode.make(response.text)
            qr_img.save("QR.png")
            print("image saved", flush=True)

            # Round the image
            pixmap = QPixmap("QR.png").scaled(370, 370)
            rounded_pixmap = self.round_image(pixmap, 40)
            self.imageLabel.setPixmap(rounded_pixmap)

            parsing_data = get_query_string(response.text)
            session_id = parsing_data.get('sessionId', [None])[0]
            print(f"Parsed session ID: {session_id}", flush=True)
            return session_id

        except Exception as e:
            print(f"Failed to fetch session ID: {e}", flush=True)
            return None

    def round_image(self, pixmap, radius):
        print(f"Rounding image with radius: {radius}", flush=True)
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
        print("Rounded image created.", flush=True)
        return rounded

    def handle_websocket_message(self, message):
        message_dict = json.loads(message)
        user_uuid = message_dict.get('senderId')
        print(f"Parsed user UUID: {user_uuid}", flush=True)
        self.open_timer_page(user_uuid)

    def open_timer_page(self, user_uuid):
        self.timer_page = Timer(self.exType, user_uuid, self.widget)
        self.widget.addWidget(self.timer_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    mainWindow = QR_Page("SITUP", widget)
    widget.addWidget(mainWindow)
    widget.setCurrentIndex(0)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    widget.show()
    sys.exit(app.exec_())
