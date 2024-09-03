import sys
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from CountDown_Page import CountDown_Page
from SerialThread import SerialThread

class Explanation(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Explanation_Page_UI.ui", self)

        self.pushButton.setStyleSheet("""
        QPushButton {
            color: #FFFFFF;
            background-color: #2463AC;
            border: 2px solid #2463AC;
            border-radius: 20px;
        }
        """)

        self.serial_thread = serial_thread

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.open_standard_page()

    def open_standard_page(self):
        self.serial_thread.send_data('3')
        widget.setCurrentIndex(widget.currentIndex() + 1)


class StandardPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Standard_Page_UI.ui", self)

        self.serial_thread = serial_thread
        self.serial_thread.data_received.connect(self.handle_serial_data)

    def handle_serial_data(self, data):
        if data == 'Y':
            widget.setCurrentIndex(widget.currentIndex() + 2)
        elif data == 'N':
            widget.setCurrentIndex(widget.currentIndex() + 1)


class StandardSuccessPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Success_Page.ui", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Enter 키가 눌렸습니다. Countdown 페이지로 이동합니다.", flush=True)
            widget.setCurrentIndex(widget.indexOf(countdown_page))


class ReStandardPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ReStandard_Page_UI.ui", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            serial_thread.send_data('3')
            widget.setCurrentIndex(widget.indexOf(standard_page))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    serial_thread = SerialThread(port='/dev/ttyS0', baudrate=9600, timeout=1)
    serial_thread.start()

    widget = QStackedWidget()

    main_page = Explanation()
    standard_page = StandardPage()
    restandard_page = ReStandardPage()
    success_page = StandardSuccessPage()
    countdown_page = CountDown_Page()

    widget.addWidget(main_page)
    widget.addWidget(standard_page)
    widget.addWidget(restandard_page)
    widget.addWidget(success_page)
    widget.addWidget(countdown_page)

    widget.setCurrentIndex(0)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    widget.show()

    app.aboutToQuit.connect(serial_thread.stop)

    sys.exit(app.exec_())
