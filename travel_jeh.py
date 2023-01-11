import sys
import pymysql # STEP 1
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

        #




    def showSelect(self, date):
        selectDate = date.toString(f'yyyy-MM-dd')
        # 선택한날짜(date)가 현재날짜(date.currentDate()) 보다 전이면(작으면) 날짜선택 불가
        if date < date.currentDate():
            print('현재날짜',date.currentDate().toString(f'yyyy-MM-dd'))   # 현재 날짜
            print('선택날짜',selectDate)   # 선택 한 날짜
            print('잘못된 날짜 선택')
            QtWidgets.QMessageBox.information(self, "날짜선택", "오늘 날짜 이후로 선택하세요")
        else :
            print('현재날짜',date.currentDate().toString(f'yyyy-MM-dd'))   # 현재 날짜
            print('선택날짜',selectDate)   # 선택 한 날짜
            selectJijum = self.combo.currentText()
            print(selectJijum)
            print('알맞은 날짜 선택')
            self.btn_search.setEnabled(True)
            self.date_edit.setText(date.toString(f'yy-MM-dd(ddd) / 여행지 {selectJijum} 선택'))

            # STEP 2: MySQL Connection 연결
            con = pymysql.connect(host='localhost', user='root', password='0000',
                                  db='jejudo', charset='utf8')  # 한글처리 (charset = 'utf8')
            # STEP 3: Connection 으로부터 Cursor 생성
            cur = con.cursor()
            # STEP 4: SQL문 실행 및 Fetch
            # 해당 하는 날짜의 '강수량'으로 비/눈이 왔던 날의 갯수 세기
            Rcnt = f"SELECT jijum_name, jeju_date, ifnull(count(rain_mm),0) FROM jejudo.jejudoweather WHERE jijum_name = '{selectJijum}' AND jeju_date LIKE '%{selectDate[5:]}' AND rain_mm > 0"
            cur.execute(Rcnt)
            RcntRows = cur.fetchall() # 데이타 Fetch
            print(RcntRows)  # 전체 rows

            # 해당 하는 날짜의 '강수량'으로 해당 날짜의 평균 강수량 계산하기
            avgRain = f"SELECT jijum_name, jeju_date, ifnull(round(avg(rain_mm),1),0) FROM jejudo.jejudoweather WHERE jijum_name = '{selectJijum}' AND jeju_date LIKE '%{selectDate[5:]}' AND rain_mm > 0"
            cur.execute(avgRain)
            avgRainRows = cur.fetchall() # 데이타 Fetch
            print(avgRainRows)  # 전체 rows

            # 해당 하는 날짜의 '일최심적설량'으로 해당 날짜의 평균 일최심적설량 계산하기
            avgSnow = f"SELECT jijum_name, jeju_date, ifnull(round(avg(snow),1),0) FROM jejudo.jejudoweather WHERE jijum_name = '{selectJijum}' AND jeju_date LIKE '%{selectDate[5:]}' AND snow > 0"
            cur.execute(avgSnow)
            avgSnowRows = cur.fetchall() # 데이타 Fetch
            print(avgSnowRows)  # 전체 rows

            # 해당 하는 날짜의 '최고기온'으로 해당 날짜의 평균 최고기온 계산하기
            maxAvgTemp = f"SELECT jijum_name, jeju_date, round(avg(maxi_temp),1) FROM jejudo.jejudoweather WHERE jijum_name = '{selectJijum}' AND jeju_date LIKE '%{selectDate[5:]}'"
            cur.execute(maxAvgTemp)
            maxAvgTempRows = cur.fetchall() # 데이타 Fetch
            print(maxAvgTempRows)  # 전체 rows

            # 해당 하는 날짜의 '최저기온'으로 해당 날짜의 평균 최저기온 계산하기
            minAvgTemp = f"SELECT jijum_name, jeju_date, round(avg(mini_temp),1) FROM jejudo.jejudoweather WHERE jijum_name = '{selectJijum}' AND jeju_date LIKE '%{selectDate[5:]}'"
            cur.execute(minAvgTemp)
            minAvgTempRows = cur.fetchall() # 데이타 Fetch
            print(minAvgTempRows)  # 전체 rows

            self.textBrowser.setText(f'과거 10년간 오늘 날짜에는\n비 또는 눈이 {RcntRows[0][2]}번 왔습니다.\n'
                                     f'평균 강수량 {avgRainRows[0][2]}mm\n'
                                     f'평균 일최심적설량 {avgSnowRows[0][2]}cm\n'
                                     f'평균 최고기온 {maxAvgTempRows[0][2]}°C\n평균 최저기온 {minAvgTempRows[0][2]}°C\n'
                                     )
            if avgRainRows[0][2] >= 80 or avgSnowRows[0][2] > 0 or maxAvgTempRows[0][2] >= 30:
                if avgRainRows[0][2] >= 80:
                    self.textBrowser.append("일 평균 강수량이 80mm 이상이므로 폭우가 올 확률이 높으니, 실내 여행지를 추천합니다.")
                elif avgSnowRows[0][2] > 0:
                    self.textBrowser.append("쌓여있는 눈이 0cm 초과이므로 미끄러울 수 있으니, 실내 여행지를 추천합니다.")
                elif maxAvgTempRows[0][2] >= 30:
                    self.textBrowser.append("평균 최고기온이 30도 이상이므로 더우니, 실내 여행지를 추천합니다.")
                data = f"SELECT * FROM jejudo.tour WHERE area = '{selectJijum}' AND indoor = '실내'"
                cur.execute(data)
                dataRows = cur.fetchall()
                print(dataRows)
                # 행 갯수 정하기
                self.table.setRowCount(len(dataRows))
                # self.table에 데이터 넣기
                for i in range(len(dataRows)):
                    self.table.setItem(i, 0, QTableWidgetItem(dataRows[i][2]))
                    self.table.setItem(i, 1, QTableWidgetItem(dataRows[i][3]))
                    self.table.setItem(i, 2, QTableWidgetItem(dataRows[i][4]))
                    # 셀 크기 조절
                    self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                    self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            else :
                self.textBrowser.append("날씨가 좋을 확률이 높으니 실외 여행지를 추천합니다.")
                # 선택 지점 tour 데이터 뽑아오기
                data = f"SELECT * FROM jejudo.tour WHERE area = '{selectJijum}' AND indoor = '실외'"
                cur.execute(data)
                dataRows = cur.fetchall()
                # for i in range(len(dataRows)):
                    # print(dataRows[i][1])  # 실내외 여부
                    # print(dataRows[i][2])   # 관광지명
                    # print(dataRows[i][3])   # 설명
                # 행 갯수 정하기
                self.table.setRowCount(len(dataRows))
                # self.table에 데이터 넣기
                for i in range(len(dataRows)):
                    self.table.setItem(i, 0, QTableWidgetItem(dataRows[i][2]))
                    self.table.setItem(i, 1, QTableWidgetItem(dataRows[i][3]))
                    self.table.setItem(i, 2, QTableWidgetItem(dataRows[i][4]))
                    # 셀 크기 조절
                    self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                    self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)













                # STEP 5: DB 연결 종료
                con.close()

    def search(self):   # 조회버튼 누르면 실행될 메서드
        self.stackedWidget.setCurrentIndex(1) # 조회버튼 누르면 다음페이지로



    def main(self):
        self.stackedWidget.setCurrentIndex(0)  # 홈버튼 누르면 메인페이지로
        self.btn_search.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
