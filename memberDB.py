import pymysql

dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')

print("1 : 회원 가입")
print("2 : 회원 비밀번호 수정")
print("3 : 회원 정보 삭제")
print("4 : 회원 리스트 조회")

menu = input("위 메뉴 중 한 가지를 선택해주세요(1~4) : ")

if menu == '1':
    print("------ 회원가입 ------")
    memberid = input("1) 회원아이디 : ")
    memberpw = input("2) 회원비밀번호 : ")
    membername = input("3) 회원이름 : ")
    memberage = input("4) 회원나이 : ")

    sql = f"INSERT INTO pymember VALUES('{memberid}','{memberpw}','{membername}','{memberage}')"

elif menu == '2':
    print("------ 회원비밀번호 수정 ------")
    memberid = input("비밀번호를 수정하실 회원의 아이디를 입력하세요 : ")
    memberpw = input("수정하실 비밀번호를 입력하세요 : ")

    sql = f"UPDATE pymember SET memberpw='{memberpw}' WHERE memberid='{memberid}'"

elif menu == '3':
    print("------ 회원 삭제 ------")
    memberid = input("탈퇴할 회원의 아이디를 입력하세요 : ")

    sql = f"DELETE FROM pymember WHERE memberid='{memberid}'"

else:
    print("***** 잘못된 번호입니다. 프로그램을 종료합니다. *****")

# 위에서 만들어진 sql문을 실행하는 구문

cur = dbConn.cursor()  # sql문을 실행시켜줄 커넥션내의 함수 호출
cur.execute(sql)  # sql문이 지정된 데이터베이스에서 실행됨

cur.close()
dbConn.commit()
dbConn.close()
