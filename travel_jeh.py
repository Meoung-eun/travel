import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5 import QtWidgets



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui_jeju.ui", self)
        self.show()
        # 스택인덱스 0으로 고정
        self.stackedWidget.setCurrentIndex(0)

        self.btn_search.clicked.connect(self.search)
        self.btn_home.clicked.connect(self.main)
        self.cal_widget.clicked[QDate].connect(self.showSelect)

        # self.textBrowser.setText('가나달마ㅏ바사ㅏㅁ사덧바서ㅏ지덧ㅈ사ㅓㅁㄹㄴㅇㄹㄴㅁㄹㄴㅁㄹㄴ멀이마ㅓ리안ㅁ')




    def showSelect(self, date):
            # 선택한날짜(date)가 현재날짜(date.currentDate()) 보다 전이면(작으면) 날짜선택 불가
            if date < date.currentDate():
                print('이전날짜선택')
                QtWidgets.QMessageBox.information(self, "날짜선택", "오늘 날짜 이후로 선택하세요")
            else :
                print('현재시각',date.currentDate())
                select = self.combo.currentText()
                self.date_edit.setText(date.toString(f'yy-MM-dd(ddd) / 여행지 {select} 선택'))



    def search(self):
        self.stackedWidget.setCurrentIndex(1) # 조회버튼 누르면 다음페이지로

    def main(self):
        self.stackedWidget.setCurrentIndex(0)  # 홈버튼 누르면 메인페이지로










if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
