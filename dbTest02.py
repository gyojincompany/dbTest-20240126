import pymysql  # mysql과 연동을 해주는 모듈 PyMySQL 설치

# 파이썬 프로그램과 데이터베이스 간의 커넥션 생성
# 1) 데이터베이스가 설치된 컴퓨터의 ip주소(내 컴퓨터에 데이터베이스가 설치되어 있으면 localhost)
# 2) 데이터베이스 계정 아이디(ex:root)
# 3) 데이터베이스 계정 비밀번호(ex:12345)
# 4) 데이터베이스의 스키마 이름(ex:pydb)

dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='pydb')
# db와의 connection 생성

# sql = "SELECT * FROM pymember"  # db에 실행할 sql문 생성

sql = "INSERT INTO pymember VALUES('whitedog','88888','이순신',55)"

cur = dbConn.cursor()  # sql문을 실행시켜줄 커넥션내의 함수 호출
cur.execute(sql)  # sql문이 지정된 데이터베이스에서 실행됨

# records = cur.fetchall()  # sql문에서 실행된 select의 모든 결과가 튜플로 반환됨
#
# print(records)  # 모든 레코드 출력
# print(records[1])  # 특정 레코드 1개만 출력

# dbConn 사용 후 반드시 닫아줄 것(순서:cur 닫아준 후 dbConn을 닫아야 함)
cur.close()
dbConn.commit()  # insert, delete, update 문을 사용했을 경우에는 반드시 commit 해줘야 함!!
dbConn.close()