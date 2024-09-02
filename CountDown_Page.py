import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui
from Main_Page import Main
from SerialThread import SerialThread

class CountDown_Page(QMainWindow):
    def __init__(self, exType, user_uuid, timertext, parent=None):
        super().__init__(parent)

        # 전달받은 값 저장
        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext

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

        self.serial_thread = SerialThread()  # SerialThread 인스턴스 생성
        self.serial_thread.start()  # SerialThread 시작

        self.start_timer()

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
        self.serial_thread.send_data('1')  # 시리얼로 1 전송
        self.main_page = Main(self.exType, self.user_uuid, self.timertext)
        self.main_page.show()
        self.close()

    def closeEvent(self, event):
        self.serial_thread.stop()  # 윈도우 종료 시 SerialThread 정리
        self.serial_thread.wait()  # SerialThread 종료 대기
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CountDown_Page(exType='exercise', user_uuid='1234', timertext=60000)
    mainWindow.show()
    sys.exit(app.exec_())
