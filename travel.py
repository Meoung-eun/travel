import sys
import pymysql # STEP 1
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5 import QtWidgets
## 그래프 관련 임포트
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui_jeju.ui", self)
        self.show()
        ## 스택인덱스 0으로 고정
        self.stackedWidget.setCurrentIndex(0)
        ## 체크가 된 item 이 담긴 리스트
        self.item_list = []
        # self.schedulelist = [] #스케줄에 넣을 리스트
        self.selectDateli = []
        self.list = []
        self.test=[]
        ## 체크가 된(삭제할) 아이템이 담긴 리스트
        self.dellist=[]
        ## 위젯 매서드와 연결(connect)
        # '홈 버튼' 클릭 할때 매서드: 메인페이지(스택0)으로이동
        self.btn_home.clicked.connect(self.main)
        # 캘린더위젯 날짜 선택 할 때 매서드: 스택1에 있는 위젯이 바뀜
        self.cal_widget.clicked[QDate].connect(self.showSelect)
        # '조회하기 버튼' 클릭 할때 매서드: 조회하기(스택1)페이지로 이동
        self.btn_search.clicked.connect(self.search)
        # '일정 추가 버튼' 클릭 할때 매서드: db에 일정이 추가됨
        self.btn_scheduleAdd.clicked.connect(self.scheduleAdd)
        # '일정조회 버튼' 클릭 할때 매서드: 일정조회(스택2)페이지로 이동
        self.btn_schedule.clicked.connect(self.scheduleSearch)
        # 'btn_del(일정삭제) 버튼 ' 클릭할때 매서드
        self.btn_del.clicked.connect(self.scheduleDel)

        ########그래프
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.vertical.addWidget(self.canvas)






    def showSelect(self, date):
        self.selectDate = date.toString(f'yyyy-MM-dd')          #'2023-01-01'
        # 선택한날짜(date)가 현재날짜(date.currentDate()) 보다 전이면(작으면) 날짜선택 불가
        if date < date.currentDate():
            print('현재날짜',date.currentDate().toString(f'yyyy-MM-dd'))   # 현재 날짜
            print('선택날짜',self.selectDate)   # 선택 한 날짜
            print('잘못된 날짜 선택')
            QtWidgets.QMessageBox.information(self, "날짜선택", "오늘 날짜 이후로 선택하세요")
        else :
            print('현재날짜',date.currentDate().toString(f'yyyy-MM-dd'))   # 현재 날짜
            print('선택날짜',self.selectDate)   # 선택 한 날짜
            self.selectJijum = self.combo.currentText()
            print(self.selectJijum)
            print('알맞은 날짜 선택')
            self.selectDateli.append(self.selectDate)
            print('날짜선택리스트',self.selectDateli)
            self.btn_search.setEnabled(True)
            self.date_edit.setText(date.toString(f'yy-MM-dd(ddd) / 여행지 {self.selectJijum} 선택'))

            # STEP 2: MySQL Connection 연결
            con = pymysql.connect(host='localhost', user='root', password='0000',
                                  db='jejudo', charset='utf8')  # 한글처리 (charset = 'utf8')
            # STEP 3: Connection 으로부터 Cursor 생성
            cur = con.cursor()
            # STEP 4: SQL문 실행 및 Fetch
            # 해당 하는 날짜의 '강수량'으로 비/눈이 왔던 날의 갯수 세기
            Rcnt = f"SELECT jijum_name, jeju_date, ifnull(count(rain_mm),0) FROM jejudo.jejudoweather WHERE jijum_name = '{self.selectJijum}' AND jeju_date LIKE '%{self.selectDate[5:]}' AND rain_mm > 0"
            cur.execute(Rcnt)
            RcntRows = cur.fetchall() # 데이타 Fetch
            print(RcntRows)  # 전체 rows

            # 해당 하는 날짜의 '강수량'으로 해당 날짜의 평균 강수량 계산하기
            avgRain = f"SELECT jijum_name, jeju_date, ifnull(round(avg(rain_mm),1),0) FROM jejudo.jejudoweather WHERE jijum_name = '{self.selectJijum}' AND jeju_date LIKE '%{self.selectDate[5:]}' AND rain_mm > 0"
            cur.execute(avgRain)
            avgRainRows = cur.fetchall() # 데이타 Fetch
            print(avgRainRows)  # 전체 rows

            # 해당 하는 날짜의 '일최심적설량'으로 해당 날짜의 평균 일최심적설량 계산하기
            avgSnow = f"SELECT jijum_name, jeju_date, ifnull(round(avg(snow),1),0) FROM jejudo.jejudoweather WHERE jijum_name = '{self.selectJijum}' AND jeju_date LIKE '%{self.selectDate[5:]}' AND snow > 0"
            cur.execute(avgSnow)
            avgSnowRows = cur.fetchall() # 데이타 Fetch
            print(avgSnowRows)  # 전체 rows

            # 해당 하는 날짜의 '최고기온'으로 해당 날짜의 평균 최고기온 계산하기
            maxAvgTemp = f"SELECT jijum_name, jeju_date, round(avg(maxi_temp),1) FROM jejudo.jejudoweather WHERE jijum_name = '{self.selectJijum}' AND jeju_date LIKE '%{self.selectDate[5:]}'"
            cur.execute(maxAvgTemp)
            maxAvgTempRows = cur.fetchall() # 데이타 Fetch
            print(maxAvgTempRows)  # 전체 rows

            # 해당 하는 날짜의 '최저기온'으로 해당 날짜의 평균 최저기온 계산하기
            minAvgTemp = f"SELECT jijum_name, jeju_date, round(avg(mini_temp),1) FROM jejudo.jejudoweather WHERE jijum_name = '{self.selectJijum}' AND jeju_date LIKE '%{self.selectDate[5:]}'"
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
                data = f"SELECT * FROM jejudo.tour WHERE area = '{self.selectJijum}' AND indoor = '실내'"
                cur.execute(data)
                self.dataRows = cur.fetchall()
                print(self.dataRows)
                # 행 갯수 정하기
                self.table.setRowCount(len(self.dataRows))
                # self.table에 데이터 넣기
                self.ckList = []
                for i in range(len(self.dataRows)):
                    self.ckBox = QCheckBox()
                    self.ckList.append(self.ckBox)
                    self.ckBox.stateChanged.connect(self.get_checked)  # 체크박스를 누를 때마다 실행되는 매서드
                    self.table.setCellWidget(i, 0, self.ckList[i])
                    self.table.setItem(i, 1, QTableWidgetItem(self.dataRows[i][2]))
                    self.table.setItem(i, 2, QTableWidgetItem(self.dataRows[i][3]))
                    self.table.setItem(i, 3, QTableWidgetItem(self.dataRows[i][4]))
                    # 셀 크기 조절
                    self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                    self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

            else :
                self.textBrowser.append("날씨가 좋을 확률이 높으니 실외 여행지를 추천합니다.")
                # 선택 지점 tour 데이터 뽑아오기
                data = f"SELECT * FROM jejudo.tour WHERE area = '{self.selectJijum}' AND indoor = '실외'"
                cur.execute(data)
                self.dataRows = cur.fetchall()
                print(self.dataRows)
                # 행 갯수 정하기
                self.table.setRowCount(len(self.dataRows))
                # self.table에 데이터 넣기
                self.ckList = []
                for i in range(len(self.dataRows)):
                    self.ckBox = QCheckBox()
                    self.ckList.append(self.ckBox)
                    self.ckBox.stateChanged.connect(self.get_checked)  # 체크박스를 누를 때마다 실행되는 매서드
                    self.table.setCellWidget(i, 0, self.ckList[i])
                    self.table.setItem(i, 1, QTableWidgetItem(self.dataRows[i][2]))
                    self.table.setItem(i, 2, QTableWidgetItem(self.dataRows[i][3]))
                    self.table.setItem(i, 3, QTableWidgetItem(self.dataRows[i][4]))
                    # 셀 크기 조절
                    self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
                    self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                    self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)



        # # STEP 5: DB 연결 종료
        # con.close()

    def get_checked(self):  # 체크박스를 누를 때마다 실행되는 매서드

        # self.item_list = []    # 체크가된 item이 담긴 리스트. 생성자에 추가함
        print('체크박스누름',end=" ")
        checkbox = self.sender()
        print(checkbox)
        item = self.table.indexAt(checkbox.pos())
        # print(item)
        item = (self.table.item(item.row(), 1).text())
        print(item)



        if item not in self.item_list:  # 아이템이 체크한 리스트에 없을 때 self.item_list에 넣음
            print('체크가됨')
            self.item_list.append(item)
            self.selectDateli.append(self.selectDate)
            print(self.item_list)
            print(self.selectDate)
            # 체크한 리스트에 있을 때 btn_scheduleAdd(일정추가버튼) 활성화
            self.btn_scheduleAdd.setEnabled(True)

        else:
            self.item_list.remove(item)
            self.selectDateli.remove(self.selectDate)
            print('체크해제')
            print(self.item_list)
            # print(self.selectDate)
            if self.item_list == []:  # 체크한 리스트가 비었을 때 버튼 비활성화
                self.btn_scheduleAdd.setEnabled(False)


        print('최종리스트',self.item_list)
        print('최종날짜리스트',self.selectDateli)
        print("체크박스개수", len(self.item_list))



    def scheduleAdd(self):      # 일정 추가하기 버튼
        self.list.clear()
        print('일정 추가')

        currentDate = self.selectDateli.pop()

        con = pymysql.connect(host='localhost', user='root', password='0000',
                              db='jejudo', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()

        for i in range(len(self.item_list)):
            data = f"SELECT * FROM jejudo.tour WHERE tour_site = '{self.item_list[i]}'"
            cur.execute(data)
            self.schedule = cur.fetchall()
            self.list.append(self.schedule)

        print('db에 추가할 리스트',self.list)
        # print('db에 추가할 리스트', self.item_list)




        # 선택한 날짜와 self.list 안에 있는 요소를 jejudo.schedule에 추가해야된다
        for i in range(len(self.list)):
            self.area = self.list[i][0][0]
            self.indoor = self.list[i][0][1]
            self.tour_site = self.list[i][0][2]
            self.explain = self.list[i][0][3]
            self.elec_charger = self.list[i][0][4]



            schedule = f"INSERT INTO jejudo.schedule (tour_date, area, indoor, tour_site, ex, elec_charger) VALUES ('{currentDate}','{self.area}','{self.indoor}','{self.tour_site}','{self.explain}','{self.elec_charger}')"
            cur.execute(schedule)
            con.commit()
            schedule2 = f"SELECT * FROM jejudo.schedule"
            cur.execute(schedule2)
            self.scheduleRows = cur.fetchall()
            con.commit()
        print('현재db jejudo.schedule 상태',self.scheduleRows)





    def scheduleSearch(self):     # 일정조회 버튼 눌렀을 때 일정조회 테이블에 schedule디비 내용 불러와서 내용 넣음
        print('일정조회')
        self.stackedWidget.setCurrentIndex(2)
        self.btn_schedule.hide()

        con = pymysql.connect(host='localhost', user='root', password='0000',
                              db='jejudo', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()

        cur.execute("SELECT DISTINCT * FROM jejudo.schedule order by tour_date")
        self.scOpenRows = cur.fetchall()
        print(self.scOpenRows)
        self.table_scedule.setRowCount(len(self.scOpenRows))
        ckList123 = []

        for i in range(len(self.scOpenRows)):
            self.ckBox456 = QCheckBox()
            ckList123.append(self.ckBox456)
            self.ckBox456.stateChanged.connect(self.get_checked_del)  # 체크박스를 누를 때마다 실행되는 매서드
            self.table_scedule.setCellWidget(i, 0, ckList123[i])
            self.table_scedule.setItem(i, 1, QTableWidgetItem(self.scOpenRows[i][0]))
            self.table_scedule.setItem(i, 2, QTableWidgetItem(self.scOpenRows[i][1]))
            self.table_scedule.setItem(i, 3, QTableWidgetItem(self.scOpenRows[i][2]))
            self.table_scedule.setItem(i, 4, QTableWidgetItem(self.scOpenRows[i][3]))
            self.table_scedule.setItem(i, 5, QTableWidgetItem(self.scOpenRows[i][4]))
            self.table_scedule.setItem(i, 6, QTableWidgetItem(self.scOpenRows[i][5]))

            # 셀 크기 조절
            self.table_scedule.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.table_scedule.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.table_scedule.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.table_scedule.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.table_scedule.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
            self.table_scedule.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
            self.table_scedule.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)

        con.commit()










    def get_checked_del(self):          # 일정조회 테이블에서 체크박스 누를때마다 실행되는 매서드

        print('삭제할거임')
        self.btn_del.setEnabled(True)
        checkbox = self.sender()
        item = self.table_scedule.indexAt(checkbox.pos())

        delitem = ((self.table_scedule.item(item.row(), 1).text()),(self.table_scedule.item(item.row(), 2).text()),
                  (self.table_scedule.item(item.row(), 3).text()),(self.table_scedule.item(item.row(), 4).text()),
                   (self.table_scedule.item(item.row(), 5).text()),(self.table_scedule.item(item.row(), 6).text()))

        if delitem not in self.dellist:
            self.dellist.append(delitem)
            print('삭제리스트',self.dellist)
        else:
            self.dellist.remove(delitem)
            print('체크해제')
            print('삭제리스트',self.dellist)


    def scheduleDel(self):
        print('db에서 삭제')
        print('삭제')

        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                               charset='utf8')
        cur = conn.cursor()
        if self.dellist != []:
            for i in range(len(self.dellist)):
                cur.execute(f" DELETE FROM jejudo.schedule WHERE tour_date = '{self.dellist[i][0]}' and area = '{self.dellist[i][1]}' and indoor = '{self.dellist[i][2]}' \
                            and tour_site = '{self.dellist[i][3]}' and ex = '{self.dellist[i][4]}' and elec_charger = '{self.dellist[i][5]}' ")
                print(self.dellist[0])
                conn.commit()
                cur.execute("select * from jejudo.schedule")
        print("집가고싶다",self.dellist)

        # 데이터를 sql에 반영
        conn.commit()
        # # Connection 닫기
        conn.close()
        # 테이블 헤더를 제외한 데이터 삭제
        self.table_scedule.clearContents()
        # 테이블 안에 데이터 생성
        self.scheduleSearch()







    def search(self):   # 조회버튼 누르면 실행될 메서드
        self.stackedWidget.setCurrentIndex(1) # 조회버튼 누르면 다음페이지로
        self.btn_scheduleAdd.setEnabled(True)


                   ##################### #### 그래프
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo', charset='utf8')
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()

        sql = f"SELECT aver_temp, jeju_date FROM jejudo.jejudoweather where jeju_date like '%{self.selectDate[5:]}' and jijum_name = '{self.selectJijum}'"
        cur.execute(sql)
        average = cur.fetchall()
        print(average)
        average_temp_list = []
        for i in average:
            average_temp_list.append(float(i[0]))
        print(average_temp_list)
        year_list = []
        for i in average:
            year_list.append(i[1])
        print(year_list)
        year_only_list = []
        for i in year_list:
            year_only_list.append(int(i[0:4]))
        print(year_only_list)

        sql = f"SELECT rain_mm FROM jejudoweather where jeju_date like '%{self.selectDate[5:]}' and jijum_name = '{self.selectJijum}'"
        cur.execute(sql)
        average1 = cur.fetchall()
        print(average1)
        average_rain_list = []
        for i in average1:
            average_rain_list.append(i[0])
        print(average_rain_list)

        ###########################
        import numpy as np

        x = np.array(year_only_list)
        print(x, np)
        print(year_only_list, 'graph')
        y1 = np.array(average_temp_list)
        y2 = np.array(average_rain_list)

        self.ax1 = self.fig.add_subplot(111)

        self.ax1.plot(x, y1, label="Temperature", color='green')
        self.ax1.set_ylabel('Temperature')

        # self.ax1.plot(x, y2, label="Rainfall", color='deeppink')
        self.ax1.set_xlabel("x")
        self.ax1.set_xlabel("y")

        self.ax1.set_title("Temperature & Rainfall")
        self.ax1.legend(loc='lower left')
        self.ax2 = self.ax1.twinx()     #그래프합치기
        self.ax1.set_zorder(self.ax2.get_zorder() + 50)     #zorder가 낮을수록 먼저 그려지고, zorder가 높을수록 나중에 그려짐
        self.ax1.patch.set_visible(False)

        self.ax2 = self.ax1.twinx()
        self.ax2.bar(x, y2, label="Rainfall", color='deeppink')
        self.ax2.legend(loc='lower right')
        self.ax2.set_ylabel('Rainfall')
        self.canvas.draw()




    def main(self):
        self.stackedWidget.setCurrentIndex(0)  # 홈버튼 누르면 메인페이지로
        self.btn_search.setEnabled(False)
        self.btn_scheduleAdd.setEnabled(False)
        self.btn_schedule.show()
        self.item_list=[]
        # self.selectDateli=[]

        #####그래프
        self.canvas.close()
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.vertical.addWidget(self.canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
