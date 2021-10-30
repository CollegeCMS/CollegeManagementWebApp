from CollegeManagement.connection import createConnection
def getsubjectid(id):
    try:
        db,cmd=createConnection()
        cmd.execute(f"select subjectid,name from subjects where facultyid={id}")
        data=cmd.fetchall()
        cmd.close()
        db.close()
        return True,data
    except Exception as e:
        return [False]