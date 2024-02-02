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
        self.login_btn.clicked.connect(self.memberLogin)  # 로그인 버튼이 클릭되면 로그인 성공여부 확인
        self.loginreset_btn.clicked.connect(self.loginReset)  # 로그인탭에서 초기화 클릭시 모든 입력사항 삭제

        # 회원 조회 버튼 클릭시 memberSearch 함수 호출
        self.membersearch_btn.clicked.connect(self.memberSearch)
        # 회원 조회 화면 초기화 버튼 클릭시 searchReset 함수 호출
        self.memberreset_btn.clicked.connect(self.searchReset)
        # 회원 조회 화면 정보수정 버튼 클릭시 memberModify 함수 호출
        self.membermodify_btn.clicked.connect(self.memberModify)


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
            QMessageBox.warning(self, "가입실패!", "회원 가입이 실패하였습니다.\n다시 가입해주세요.")

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
            QMessageBox.warning(self, "회원 가입 불가", "입력하신 아이디는 이미 존재하는 아이디입니다.\n다른 아이디를 입력하세요.")
        else:
            QMessageBox.warning(self, "회원 가입 가능", "입력하신 아이디는 가입가능한 아이디입니다.\n계속해서 가입 진행하세요.")

        cur.close()
        dbConn.close()

    def memberLogin(self):
        memberid = self.loginid_edit.text()
        memberpw = self.loginpw_edit.text()
        dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
        sql = f"SELECT * FROM appmember WHERE memberid='{memberid}' AND memberpw='{memberpw}'"

        cur = dbConn.cursor()
        cur.execute(sql)

        result = cur.fetchone()
        # print(result)

        if result != None:  # 참이면 현재 조회하려는 아이디가 DB에 이미 존재함
            QMessageBox.warning(self, "로그인 성공!", f"{result[2]}님 환영합니다.\n로그인 하셨습니다.")
            self.loginReset()
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호가 틀립니다.\n다시 확인후 로그인하세요.")

        cur.close()
        dbConn.close()

    def loginReset(self):
        self.loginid_edit.clear()  # loginid_edit 입력된 텍스트를 삭제
        self.loginpw_edit.clear()  # loginpw_edit 입력된 텍스트를 삭제

    def memberSearch(self):  # 회원 조회 함수
        memberid = self.memberid_edit.text()  # 유저가 조회하기 위해 입력한 아이디 가져오기

        dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
        sql = f"SELECT * FROM appmember WHERE memberid='{memberid}'"

        cur = dbConn.cursor()
        cur.execute(sql)

        result = cur.fetchone()

        cur.close()
        dbConn.close()

        print(result)  # result는 튜플구조로 인덱스를 사용하여 참조 가능

        if result != None:  # 회원 가입 여부 확인->조건이 참이면 등록된 회원임
            self.memberpw_edit.setText(result[1])
            self.membername_edit.setText(result[2])
            self.memberemail_edit.setText(result[3])
            self.memberage_edit.setText(str(result[4]))
        else:
            QMessageBox.warning(self, '아이디 오류', '조회하신 아이디는 없는 아이디입니다.\n다시확인해 주세요.')

    def searchReset(self):  # 회원조회 화면에서 모든 항목을 초기화
        self.memberid_edit.clear()
        self.memberpw_edit.clear()
        self.membername_edit.clear()
        self.memberemail_edit.clear()
        self.memberage_edit.clear()

    def memberModify(self):  # 회원정보 수정 함수
        
        # 현재 입력되어 있는 회원정보를 모두 가져오기
        memberid = self.memberid_edit.text()
        memberpw = self.memberpw_edit.text()
        membername = self.membername_edit.text()
        memberemail = self.memberemail_edit.text()
        memberage = self.memberage_edit.text()

        dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
        sql = f"UPDATE appmember SET memberpw='{memberpw}', membername='{membername}', memberemail='{memberemail}', memberage='{memberage}' WHERE memberid='{memberid}'"

        cur = dbConn.cursor()
        result = cur.execute(sql)  # 성공시 1이 반환

        if result == 1:  # 회원정보 수정  성공
            QMessageBox.warning(self, '회원정보수정 성공', '입력하신 정보로 회원정보가 수정되었습니다.')
        else:  # 회원정보 수정 실패
            QMessageBox.warning(self, '회원정보수정 실패', '입력하신 정보로 회원정보가 수정이 실패하였습니다.')


        cur.close()
        dbConn.commit()  # insert, delete, update 문은 꼭 실행후 commit 해줘야 함!!!
        dbConn.close()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())