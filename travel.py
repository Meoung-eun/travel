from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui_jeju.ui", self)
        self.show()
        self.btn_search.clicked.connect(self.search)
        self.btn_home.clicked.connect(self.main)
        # self.combo.currentIndexChanged.connect(self.combobox)

        # # CalendarWidget에서 날짜가 클릭되었을 때 기능 실행
        # self.cal_widget.clicked.connect(Calendar)
        # # CalendarWidget에서 선택된 날짜가 바뀌었을 때 기능 실행
        # self.cal_widget.selectionChanged.connect(Calendar2)
        # # CalendarWidget에서 달력을 다른 페이지로 넘겼을 때 기능 실행
        # self.cal_widget.currentPageChanged.connect(Calendar3)

    def search(self):
        self.stackedWidget.setCurrentIndex(1) # 조회버튼 누르면 다음페이지로

    def main(self):
        self.stackedWidget.setCurrentIndex(0)  # 홈버튼 누르면 메인페이지로
    # def combobox(self):


    # def Calendar(self):
    #
    # def Calendar2(self):
    #
    # def Calendar3(self):

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
