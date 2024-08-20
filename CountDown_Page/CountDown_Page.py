import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Countdown")
        self.setGeometry(0, 0, 1920, 1080)

        self.count = 3

        self.label = QLabel(self)
        self.label.setGeometry(580, 230, 800, 500)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(str(self.count))
        self.label.setFont(QtGui.QFont("Roboto", 200))
        self.label.setStyleSheet("Color : #0C51A2")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_count)


        self.start_timer()

    def start_timer(self):
        self.timer.start(1000)

    def update_count(self):
        self.count -= 1
        self.label.setText(str(self.count))
        if self.count == 0:
            self.label.setText('Start!')
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)