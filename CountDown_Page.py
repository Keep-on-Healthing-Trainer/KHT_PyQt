import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui
from Main_Page import Main

class CountDown_Page(QMainWindow):
    def __init__(self, exType, user_uuid, timertext, arduino, widget, parent=None):
        super().__init__(parent)
        self.widget = widget

        print("cnt")
        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext
        self.arduino = arduino

        self.setWindowTitle("Countdown")
        self.setGeometry(0, 0, 1920, 1080)

        self.count = 3

        print("daa")

        self.label = QLabel(self)
        self.label.setGeometry(580, 230, 800, 500)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(str(self.count))
        self.label.setFont(QtGui.QFont("Roboto", 200))
        self.label.setStyleSheet("Color : #0C51A2")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_count)

        self.start_timer()
        print("cnt init")

    def start_timer(self):
        self.timer.start(1000)

    def update_count(self):
        self.count -= 1
        self.label.setText(str(self.count))
        if self.count == 0:
            self.label.setText('Start!')
        if self.count == -1:
            self.timer.stop()
            self.open_main_page()

    def open_main_page(self):
        self.hide()
        self.arduino.write(b'1')
        self.main_page = Main(self.exType, self.user_uuid, self.timertext, self.arduino)
        self.widget.addWidget(self.main_page)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)


    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CountDown_Page(exType='exercise', user_uuid='1234', timertext=60000)
    mainWindow.show()
    sys.exit(app.exec_())
