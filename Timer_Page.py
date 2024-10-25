import sys
import serial
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from Explanation_Page import Explanation


class Timer(QDialog):
    def __init__(self, exType, user_uuid, parent=None):
        super().__init__(parent)
        print("load Timer_Page_UI", flush=True)

        self.a = serial.Serial('COM4', 115200, timeout=1)

        try:
            uic.loadUi("Timer_Page_UI(1).ui", self)
            print("Successfully loaded Timer_Page_UI", flush=True)
        except Exception as e:
            print(f"Failed to load Timer_Page_UI: {e}", flush=True)
            return

        self.exType = exType
        self.user_uuid = user_uuid

        print(f"Received exType: {self.exType}", flush=True)
        print(f"Received user_uuid: {self.user_uuid}", flush=True)

        self.lineEdit.setFocus()

        self.lineEdit.returnPressed.connect(self.on_return_pressed)

    def on_return_pressed(self):
        self.text = self.lineEdit.text()
        print(f"Timer input received: {self.text}", flush=True)
        try:
            timertext = (int(self.text[0:2]) * 60 + int(self.text[3:])) * 1000
            print(f"Timer set for: {timertext} milliseconds", flush=True)

            self.open_explanation_page(timertext)

        except ValueError:
            print("Please enter time in mm:ss format.", flush=True)

    def open_explanation_page(self, timertext):
        self.explanation_page = Explanation(self.exType, self.user_uuid, timertext, self.a, self.parent())

        self.parent().addWidget(self.explanation_page)
        self.parent().setCurrentIndex(self.parent().currentIndex() + 1)


if __name__ == '__main__':
    print("Starting Timer application", flush=True)
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    main = Timer("SITUP", "example_sender_id")
    widget.addWidget(main)
    widget.setCurrentIndex(0)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    widget.show()
    sys.exit(app.exec_())
