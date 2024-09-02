from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.uic import loadUi
from CountDown_Page import CountDown_Page

class Explanation(QDialog):
    def __init__(self, exType, user_uuid, timertext, parent=None):
        super().__init__(parent)
        loadUi("Explanation_Page_UI.ui", self)

        self.exType = exType
        self.user_uuid = user_uuid
        self.timertext = timertext
        print(
            f"Explanation Page Initialized with exType: {self.exType}, user_uuid: {self.user_uuid}, timertext: {self.timertext}",
            flush=True)

        self.pushButton.setStyleSheet("""
        QPushButton {
            color: #FFFFFF;
            background-color: #2463AC;
            border: 2px solid #2463AC;
            border-radius: 20px;
        }
        """)

        # QPushButton 클릭 이벤트
        self.pushButton.clicked.connect(self.open_standard_page)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Enter 키가 눌렸습니다. StandardPage로 이동합니다.", flush=True)
            self.open_standard_page()

    def open_standard_page(self):
        # StandardPage로 이동
        widget.setCurrentIndex(widget.currentIndex() + 1)

class StandardPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Standard_Page_UI.ui", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Enter 키가 눌렸습니다. StandardSuccessPage로 이동합니다.", flush=True)
            self.open_success_page()

    def open_success_page(self):
        # StandardSuccessPage로 이동
        widget.setCurrentIndex(widget.currentIndex() + 2)

class StandardSuccessPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Success_Page.ui", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Enter 키가 눌렸습니다. CountDown 페이지로 이동합니다.", flush=True)
            self.open_re_page()

    def open_re_page(self):
        # StandardSuccessPage로 이동
        widget.setCurrentIndex(widget.currentIndex() - 1)

class ReStandardPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ReStandard_Page_UI.ui", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Enter 키가 눌렸습니다. StandardPage로 이동합니다.", flush=True)
            self.open_countdown_page()

    def open_countdown_page(self):
        self.hide()
        self.countdown_page = CountDown_Page(self.exType, self.user_uuid, self.timertext)
        self.countdown_page.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = QStackedWidget()

    main_page = Explanation()
    standard_page = StandardPage()
    restandard_page = ReStandardPage()
    success_page = StandardSuccessPage()

    widget.addWidget(main_page)
    widget.addWidget(standard_page)
    widget.addWidget(restandard_page)
    widget.addWidget(success_page)

    # CountDown 페이지를 직접 추가
    countdown_page = CountDown_Page()  # CountDown 인스턴스를 직접 생성
    widget.addWidget(countdown_page)

    widget.setCurrentIndex(0)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)

    widget.show()

    sys.exit(app.exec_())