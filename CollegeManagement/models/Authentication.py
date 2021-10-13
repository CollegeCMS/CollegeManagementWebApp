from .connection import createConnection
import bcrypt
from datetime import datetime
def checkCredential(id,password,table):
    try:
        db,cmd=createConnection()
        q=f"select {table}id,password from {table} where emailid='{id}'"
        print(q)
        cmd.execute(q)
        count=cmd.rowcount
        db.close()
        if(count==0):
            return False,-1
        else:
            result=cmd.fetchone()
            # res=bcrypt.checkpw(password,str(result[1]).encode())
            res=password==result['password']
            if(res):
                return True,result[f"{table}id"]
            else:
                return False,-1
    except Exception as e:
        print("Error dataBase"+str(e))
        return False,0
def FetchData(id,table):
    try:
        q=f"select * from {table} where {table}id={id}"
        print(q)
        db,cmd=createConnection()
        cmd.execute(q)
        data=cmd.fetchone()
        db.close()
        data.pop('password')
        data=isClubMember(data,id,table)
        return True,data
    except Exception as e:
        print(e)
        return False,[]
def isClubMember(data:dict,id,status):
    try:
        if(bool(data['clubmember'])):
            l=['clubid', 'clubname', 'hoc', 'hocid', 'clubcode', 'clublogo', 'numberofmember', 'goal', 'status','clubmemberid']
            db, cmd = createConnection()
            q = f"select p.*,s.* from club s,collegeclub p where s.memberid={id} and s.memberstatus='{status}' and s.clubcode=p.clubid"
            print(q)
            cmd.execute(q)
            dataClub = cmd.fetchone()
            if(dataClub):
            # dataClub = dict(zip(l, dataClub))
                data.update(dataClub)
            db.close()
        return data
    except Exception as e:
        print(e)
        return data
def saveAlert(data):
    try:
        db, cmd = createConnection()
        q = f"insert into alerts (message, memberid, time, permmision, status, memberstatus) values{data}"
        cmd.execute(q)
        db.close()
        return True
    except Exception as e:
        print(e)
        return False
def givePermission(id):
    try:
        db, cmd = createConnection()
        q = f"update alerts set status=1,permmision=0 where alertid={id}"
        cmd.execute(q)
        db.close()
        return True
    except Exception as e:
        print(e)
        return False
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
def uploadAttendenceFile(fileid,subjectid,present):
    try:
        data=getBranchandsemester(subjectid)
        branch=data['branch']
        semester=data['semester']
        if("/" in branch):
            a=tuple(branch.split('/'))
        else:
            a=f"('{branch}')"
        q=f"insert into attendencefile (filename, subjectid, date, presentstudent, absentstudent, total) values('{fileid}',{subjectid},{str(datetime.now().toordinal())},{present},(select count(*) from student where semester={semester} and branch in {a})-{present},(select count(*) from student where semester={semester} and branch in {a}))"
        print(q)
        db,cmd=createConnection()
        cmd.execute(q)
        db.commit()
        cmd.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        return False
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
def fetchAllStudent(subjectid,names):
    try:
        data = getBranchandsemester(subjectid)
        branch = data['branch']
        semester = data['semester']
        if ("/" in branch):
            a = tuple(branch.split('/'))
        else:
            a = f"('{branch}')"
        q=f"select studentid,name from student where semester={semester} and branch in {a} and name in {names}"
        print(q)
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
        db,cmd=createConnection()
        cmd.execute(q)
        data=cmd.fetchone()
        if(data):
            return True,data
        else:
            return [False]
    except Exception as e:
        print(e)
        return [False]