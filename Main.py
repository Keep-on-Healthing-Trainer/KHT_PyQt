import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Timer_Page import Timer
from CountDown_Page import CountDown

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # QStackedWidget 생성
    stacked_widget = QStackedWidget()

    # 페이지 추가
    timer_page = Timer()
    countdown_page = CountDown()

    # QStackedWidget에 페이지 등록
    stacked_widget.addWidget(timer_page)
    stacked_widget.addWidget(countdown_page)

    # 첫 번째 페이지로 설정
    stacked_widget.setCurrentIndex(0)

    # QStackedWidget 창 표시
    stacked_widget.resize(1920, 1080)  # 창 크기 설정
    stacked_widget.show()

    sys.exit(app.exec_())