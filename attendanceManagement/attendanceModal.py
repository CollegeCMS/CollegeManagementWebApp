from CollegeManagement.connection import createConnection,createConnectionList
def getBranchandsemester(subjectid):
    try:
        q=f"select branch,semester from subjects where subjectid={subjectid}"
        db,cmd=createConnection()
        cmd.execute(q)
        data=cmd.fetchone()
        cmd.close()
        db.close()
        return data
    except Exception as e:
        print(e)
        return {}
def uploadAttendenceFile(fileid,subjectid,present,date):
    try:
        data=getBranchandsemester(subjectid)
        branch=data['branch']
        semester=data['semester']
        if("/" in branch):
            a=tuple(branch.split('/'))
        else:
            a=f"('{branch}')"
        q=f"insert into attendencefile (filename, subjectid, date, presentstudent, absentstudent, total) values('{fileid}',{subjectid},{str(date)},{present},(select count(*) from student where semester={semester} and branch in {a})-{present},(select count(*) from student where semester={semester} and branch in {a}))"
        db,cmd=createConnection()
        cmd.execute(q)
        db.commit()
        cmd.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        return False
def fetchAllStudent(subjectid):
    try:
        data = getBranchandsemester(subjectid)
        branch = data['branch']
        semester = data['semester']
        if ("/" in branch):
            a = tuple(branch.split('/'))
        else:
            a = f"('{branch}')"
        # q=f"select studentid,name from student where semester={semester} and branch in {a} and name in {names}"
        q=f"select studentid,name from student where semester={semester} and branch in {a}"
        db, cmd = createConnection()
        cmd.execute(q)
        data=cmd.fetchall()
        cmd.close()
        db.close()
        return True,data
    except Exception as e:
        print(e)
        return False,[]
def getAttendence(id,date):
    try:
        q=f"select * from attendencefile where subjectid={id} and date={date}"
        q1=f"select s.studentid,s.name,(select count(*) from studentattendence where subjectid={id} and studentid=s.studentid and attendence='P' and date<={date}) present,(select count(*) from studentattendence where subjectid={id} and studentid=s.studentid and attendence='A' and date<={date}) absent from student s"
        db,cmd=createConnection()
        cmd.execute(q)
        data=cmd.fetchone()
        if(data):
            db.close()
            db,cmd=createConnectionList()
            cmd.execute(q1)
            data1=cmd.fetchall()
            return [True,data,data1]
        else:
            return [False]
    except Exception as e:
        print(e)
        return [False]
