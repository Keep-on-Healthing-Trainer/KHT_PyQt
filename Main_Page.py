import asyncio, httpx, serial
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic

class SerialWorker(QThread):
    update_count_signal = pyqtSignal(str)

    def __init__(self, arduino, parent=None):
        super().__init__(parent)
        self.arduino = arduino
        self.arduino.flushInput()

    def run(self):
        self.arduino.write(b'2')
        exercise_count = self.arduino.readline().decode().strip()
        print(f"exercise_count: {exercise_count}")

        self.update_count_signal.emit(exercise_count)

class AsyncServerWorker(QThread):
    server_response_signal = pyqtSignal(int, str)

    def __init__(self, url, data, parent=None):
        super().__init__(parent)
        self.url = url
        self.data = data

    async def send_data_to_url(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, json=self.data)
                self.server_response_signal.emit(response.status_code, response.text)
        except httpx.RequestError as e:
            print(f"An error occurred: {e}")
            self.server_response_signal.emit(-1, str(e))

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_data_to_url())
        loop.close()

class Main(QMainWindow):
    def __init__(self, exType, user_uuid, timertext, arduino, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("Main_Page_UI.ui", self)

        self.arduino = arduino
        self.timer_label = self.findChild(QLabel, "Timer")
        self.count_label = self.findChild(QLabel, "Count")
        self.kcal_label = self.findChild(QLabel, "Kcal")

        self.count_label.setText("")

        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext

        self.timer_count = int(self.timertext / 1000)
        self.kcal_value = 0
        self.exercise_count = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_count)
        self.timer.start(1000)
        self.update_timer_label()

        self.serial_worker = SerialWorker(self.arduino)
        self.serial_worker.update_count_signal.connect(self.on_count_received)

    def update_timer_count(self):
        if self.timer_count <= 0:
            print("Timer ended")
            self.timer_label.setText('00:00')
            self.serial_worker.start()
            self.timer.stop()
        else:
            self.timer_count -= 1
            self.update_timer_label()

    def update_timer_label(self):
        minutes, seconds = divmod(self.timer_count, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def on_count_received(self, exercise_count):
        self.exercise_count = int(exercise_count)
        self.update_count_label()
        self.display_kcal()

        url = f"{https://url/exercise/}{self.user_uuid}"
        data = {"count": self.exercise_count, "type": self.exType}
        self.server_worker = AsyncServerWorker(url, data)
        self.server_worker.server_response_signal.connect(self.on_server_response)
        self.server_worker.start()

    def update_count_label(self):
        self.count_label.setText(f"{self.exercise_count}")

    def display_kcal(self):
        if self.exType == "SITUP":
            self.kcal_value = self.exercise_count * 0.9
        elif self.exType == "SQUAT":
            self.kcal_value = self.exercise_count * 0.5
        elif self.exType == "PUSHUP":
            self.kcal_value = self.exercise_count * 0.4
        self.kcal_label.setText(f"{self.kcal_value:.2f}")
        print(f"Kcal: {self.kcal_value}")

    def on_server_response(self, status_code, response_text):
        if status_code == -1:
            print("Failed to send data to server:", response_text)
        else:
            print(f"Status Code: {status_code}")
            print(f"Response Text: {response_text}")

if __name__ == "__main__":
    app = QApplication([])
    arduino = serial.Serial('COM4', 115200)
    myWindow = Main(exType='SITUP', user_uuid='1234', timertext=60000, arduino=arduino)
    myWindow.show()
    app.exec_()
