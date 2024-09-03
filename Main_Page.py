import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from SerialThread import SerialThread


class Main(QMainWindow):
    def __init__(self, exType, user_uuid, timertext, parent=None):
        super().__init__(parent)

        self.ui = uic.loadUi("Main_Page_UI.ui", self)

        self.timer_label = self.findChild(QLabel, "Timer")
        self.count_label = self.findChild(QLabel, "Count")
        self.kcal_label = self.findChild(QLabel, "Kcal")

        if self.timer_label is None:
            print("Timer QLabel not found")
        if self.kcal_label is None:
            print("kcal QLabel not found")
        if self.count_label is None:
            print("Count QLabel not found")

        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext

        print(f"Main Page Initialized with exType: {self.exType}, user_uuid: {self.user_uuid}, timertext: {self.timertext}", flush=True)

        self.count = int(self.timertext / 1000)
        self.count_value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_count)
        self.timer.start(1000)
        self.update_timer_label()
        self.update_count_label()

        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.handle_serial_data)
        self.serial_thread.start()

    def update_count(self):
        self.count -= 1
        self.update_timer_label()

        if self.count <= 0:
            self.timer.stop()
            self.timer_label.setText('00:00')
            self.serial_thread.send_data('2')
            self.url = {base_url/exercise} + self.user_uuid
            print(self.url)
            self.calculate_and_display_kcal()
            self.send_data_to_url(self.url, {"count": self.count_value, "exType": self.exType})

    def update_timer_label(self):
        minutes, seconds = divmod(self.count, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def update_count_label(self):
        self.count_label.setText(f"{self.count_value}")

    def display_kcal(self):
        kcal_value = self.count_value * 0.9
        self.kcal_label.setText(f"{kcal_value:.2f}")

    def handle_serial_data(self, data):
        try:
            new_count = int(data)
            if new_count > 0:
                kcal_value = new_count * 0.9
                self.display_kcal(kcal_value)
                self.count = new_count
                self.update_timer_label()
        except ValueError:
            print(f"받은 데이터가 유효하지 않습니다: {data}")

    def send_data_to_url(self, url, data):
        try:
            response = requests.post(url, json=data)
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def closeEvent(self, event):
        self.serial_thread.stop()
        self.serial_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main(exType='exercise', user_uuid='1234', timertext=60000)
    myWindow.show()
    app.exec_()