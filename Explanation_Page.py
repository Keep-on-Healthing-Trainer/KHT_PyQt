import sys, serial
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from CountDown_Page import CountDown_Page

class Explanation(QDialog):
    def __init__(self, exType, user_uuid, timertext, Arduino, widget, parent=None):
        super().__init__(parent)
        print("exp init")
        loadUi("Explanation_Page_UI.ui", self)
        self.widget = widget
        self.pushButton.clicked.connect(self.open_standard_page)

        print("load ui")
        self.arduino = Arduino
        print("ard")
        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext

        self.pushButton.setStyleSheet(""" 
        QPushButton {
            color: #FFFFFF;
            background-color: #2463AC;
            border: 2px solid #2463AC;
            border-radius: 20px;
        }
        """)

        print(f"Received exType: {self.exType}", flush=True)
        print(f"Received user_uuid: {self.user_uuid}", flush=True)
        print(f"Received timertext: {self.timertext}", flush=True)

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            print("moving to StandardPage")
            self.open_standard_page()

    def open_standard_page(self):
        if self.arduino.is_open:
            standard_page = StandardPage(self.arduino, self.exType, self.user_uuid, self.timertext, self.widget)
            self.widget.addWidget(standard_page)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            self.hide()

class StandardPage(QDialog):
    def __init__(self, Arduino, exType, user_uuid, timertext, widget, parent=None):
        super().__init__(parent)
        print("open standard page")
        loadUi("Standard_Page_UI.ui", self)
        print("load Standard UI")
        self.widget = widget
        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext
        self.arduino = Arduino

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.check_serial_data()

    def check_serial_data(self):
        try:
            if self.arduino.is_open:
                print("arduino_open")
                Data = '3'
                self.arduino.write(b'3')
                while True:
                    self.arduino.write(Data.encode('utf-8'))
                    if self.arduino.readable():
                        data = self.arduino.readline()
                        data = data.decode('utf-8').rstrip()
                        if data == "Y":
                            print(f"data{data}")
                            standard_success_page = StandardSuccessPage(self.exType, self.user_uuid, self.timertext, self.arduino, self.widget)
                            self.widget.addWidget(standard_success_page)
                            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                            self.hide()
                            break
                        elif data == "N":
                            print(data)
                            restandard_page = ReStandardPage(self.arduino, self.widget)
                            self.widget.addWidget(restandard_page)
                            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                            self.hide()
                            break
        except serial.SerialException as e:
            print(f"Serial error: {e}")

class StandardSuccessPage(QDialog):
    def __init__(self, exType, user_uuid, timertext, arduino, widget, parent=None):
        super().__init__(parent)
        print("success")
        loadUi("Success_Page.ui", self)

        self.pushButton.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #2463AC;
                border: 2px solid #2463AC;
                border-radius: 20px;
            }
        """)

        self.widget = widget
        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext
        self.arduino = arduino
        print("init")
        self.setFocusPolicy(Qt.StrongFocus)

        self.pushButton.clicked.connect(self.open_countdown_page)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.open_countdown_page()

    def open_countdown_page(self):
        self.hide()
        countdown_page = CountDown_Page(self.exType, self.user_uuid, self.timertext, self.arduino, self.widget)
        self.widget.addWidget(countdown_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class ReStandardPage(QDialog):
    def __init__(self, arduino, widget, parent=None):
        super().__init__(parent)
        loadUi("ReStandard_Page_UI.ui", self)

        self.pushButton.setStyleSheet("""
                    QPushButton {
                        color: #FFFFFF;
                        background-color: #2463AC;
                        border: 2px solid #2463AC;
                        border-radius: 20px;
                    }
                """)

        self.arduino = arduino
        self.widget = widget
        self.setFocusPolicy(Qt.StrongFocus)

        self.pushButton.clicked.connect(self.try_again)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.try_again()

    def try_again(self):
        if self.arduino.is_open:
            self.arduino.write(b'3')
            self.hide()
            countdown_page = CountDown_Page(self.exType, self.user_uuid, self.timertext, self.arduino, self.widget)
            self.widget.addWidget(countdown_page)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    arduino = serial.Serial('COM4', 115200, timeout=1)

    exType = "ExampleType"
    user_uuid = "12345-abcde"
    timertext = "00:30"

    main_page = Explanation(exType, user_uuid, timertext, arduino, widget)

    widget.addWidget(main_page)

    widget.setCurrentIndex(0)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    widget.show()

    sys.exit(app.exec_())