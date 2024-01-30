# 회원 관리 프로그램

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

import pymysql

form_class = uic.loadUiType("ui/member.ui")[0]  # ui불러오기

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원관리 프로그램")

        self.join_btn.clicked.connect(self.memberJoin)  # 회원가입 버튼이 클릭되면 memberJoin 함수 호출
        self.joinreset_btn.clicked.connect(self.joinReset)  # 회원가입탭에서 초기화 클릭시 모든 입력사항 삭제
        self.idcheck_btn.clicked.connect(self.idCheck)
        # 현재 아이디 입력창에 입력된 아이디를 가져와 db에 존재하는지 여부 체크

    def memberJoin(self):  # 회원 가입 함수
        memberid = self.joinid_edit.text()  # 유저가 입력한 회원아이디 텍스트 가져오기
        memberpw = self.joinpw_edit.text()
        membername = self.joinname_edit.text()
        memberemail = self.joinemail_edit.text()
        memberage = self.joinage_edit.text()

        dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
        sql = f"INSERT INTO appmember VALUES ('{memberid}','{memberpw}','{membername}','{memberemail}',{memberage})"
        
        cur = dbConn.cursor()
        result = cur.execute(sql)  # 데이터 삽입이 성공하면 1이 반환

        if(result == 1):
            QMessageBox.warning(self, "가입성공!","회원 가입이 성공하였습니다.")
            self.joinReset()  # 회원 가입 성공 후에 입려된 값 초기화
        else:
            QMessageBox.warning(self, "가입실패!", "회원 가입이 실패하였습니다. 다시 가입해주세요.")

        cur.close()
        dbConn.commit()  # insert, update, delete 실행시는 반드시 commit
        dbConn.close()

    def joinReset(self):
        self.joinid_edit.clear()  # joinid_edit 입력된 텍스트를 삭제
        self.joinpw_edit.clear()
        self.joinname_edit.clear()
        self.joinemail_edit.clear()
        self.joinage_edit.clear()

    def idCheck(self):
        memberid = self.joinid_edit.text()
        dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
        sql = f"SELECT * FROM appmember WHERE memberid='{memberid}'"

        cur = dbConn.cursor()
        cur.execute(sql)

        result = cur.fetchone()

        if result != None:  # 참이면 현재 조회하려는 아이디가 DB에 이미 존재함
            QMessageBox.warning(self, "회원 가입 불가", "입력하신 아이디는 이미 존재하는 아이디입니다. 다른 아이디를 입력하세요.")
        else:
            QMessageBox.warning(self, "회원 가입 가능", "입력하신 아이디는 가입가능한 아이디입니다. 계속해서 가입 진행하세요.")

        cur.close()
        dbConn.close()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())