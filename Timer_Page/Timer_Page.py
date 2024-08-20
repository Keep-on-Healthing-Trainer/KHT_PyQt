import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

form_window = uic.loadUiType("Timer_Page_UI.ui")[0]

class Timer_Page(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Timer')

        self.lineEdit.returnPressed.connect(self.on_return_pressed)

    def on_return_pressed(self):
        self.text = self.lineEdit.text()
        self.parentWidget().setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Timer_Page()
    window.show()
    sys.exit(app.exec_())
