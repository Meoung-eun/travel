import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# ui파일 연결
form_class = uic.loadUiType("ui_jeju.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ui 시작 인덱스 0으로 고정
        self.stackedWidget.setCurrentIndex(0)

        self.btn_home.clicked.connect(self.home)
        self.btn_search.clicked.connect(self.search)

    def search(self):
        self.stackedWidget.setCurrentIndex(1)

    def home(self):
        self.stackedWidget.setCurrentIndex(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

