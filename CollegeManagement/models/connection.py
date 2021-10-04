import pymysql as sql
def createConnection(database="collegemanagement"):
    db=sql.connect(host="localhost",port=3306,password="123Nitin@456",db=database,user="root")
    cmd=db.cursor()
    return db,cmd