import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from Explanation_Page import Explanation


class Timer(QDialog):
    def __init__(self, exType, user_uuid, parent=None):
        super().__init__(parent)
        print("load Timer_Page_UI", flush=True)

        try:
            uic.loadUi("Timer_Page_UI.ui", self)
            print("Successfully loaded Timer_Page_UI", flush=True)
        except Exception as e:
            print(f"Failed to load Timer_Page_UI: {e}", flush=True)
            return

        self.exType = exType
        self.user_uuid = user_uuid

        print(f"Received exType: {self.exType}", flush=True)
        print(f"Received user_uuid: {self.user_uuid}", flush=True)

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
        print("open Explanation page", flush=True)
        self.hide()

        self.explanation_page = Explanation(self.exType, self.user_uuid, timertext)
        self.explanation_page.exec_()


if __name__ == '__main__':
    print("Starting Timer application", flush=True)
    app = QApplication(sys.argv)
    window = Timer("SITUP", "example_sender_id")
    window.show()
    sys.exit(app.exec_())
