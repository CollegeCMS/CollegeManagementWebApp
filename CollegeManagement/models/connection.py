import pymysql as sql
from ..SecretKeys.codes import codes
from sqlalchemy import create_engine
def createConnection(database="collegemanagement"):
    db=sql.connect(host="localhost",port=3306,password=codes['DB_PASSWORD'],db=database,user="root")
    cmd=db.cursor(sql.cursors.DictCursor)
    return db,cmd
def createDataConnection(database="collegemanagement"):
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw=codes['DB_PASSWORD'],
                                   db=database))
    return engine
