import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath

form_window = uic.loadUiType("Exercise_Page_UI.ui")[0]

class FocusLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.default_style = self.styleSheet()
        self.setFixedSize(350, 350)
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 30px;
            }
        """)

    def focusInEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 30px;
                border: 3px solid #0075FF;
            }
        """)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 30px;
            }
        """)
        super().focusOutEvent(event)

def round_image(self, pixmap, radius):
    size = pixmap.size()

    rounded = QPixmap(size)
    rounded.fill(Qt.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(pixmap))
    painter.setPen(Qt.NoPen)

    path = QPainterPath()
    path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)
    painter.drawPath(path)

    painter.end()
    return rounded

class DirectionalFocusWidget(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Directional Focus Widget')
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: white;")

        layout = QHBoxLayout()

        self.label1 = FocusLabel('Label 1')
        self.label2 = FocusLabel('Label 2')
        self.label3 = FocusLabel('Label 3')

        self.label1.setFocusPolicy(Qt.StrongFocus)
        self.label2.setFocusPolicy(Qt.StrongFocus)
        self.label3.setFocusPolicy(Qt.StrongFocus)

        layout.addWidget(self.label1)
        pixmap = QPixmap("situp.jpg").scaled(300, 300)
        rounded_pixmap = round_image(self, pixmap, 40)
        self.label1.setPixmap(rounded_pixmap)

        layout.addWidget(self.label2)
        pixmap = QPixmap("squat.png").scaled(300, 300)
        rounded_pixmap = round_image(self, pixmap, 40)
        self.label2.setPixmap(rounded_pixmap)

        layout.addWidget(self.label3)
        pixmap = QPixmap("pushup.jpg").scaled(300, 300)
        rounded_pixmap = round_image(self, pixmap, 40)
        self.label3.setPixmap(rounded_pixmap)

        self.setLayout(layout)

        self.label1.setFocus()

    def keyPressEvent(self, event):
        # 현재 포커스 가져오기
        focused_widget = QApplication.focusWidget()

        if event.key() == Qt.Key_Left:
            self.moveFocus(focused_widget, -1)
        elif event.key() == Qt.Key_Right:
            self.moveFocus(focused_widget, 1)

    def moveFocus(self, current_widget, direction):
        widgets = [self.label1, self.label2, self.label3]

        if current_widget in widgets:
            current_index = widgets.index(current_widget)
            next_index = (current_index + direction) % len(widgets)
            widgets[next_index].setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DirectionalFocusWidget()
    window.show()
    sys.exit(app.exec_())