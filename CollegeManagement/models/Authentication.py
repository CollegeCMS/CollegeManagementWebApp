from .connection import createConnection
import bcrypt
def checkCredential(id,password,table):
    try:
        db,cmd=createConnection()
        q=f"select {table}id,password from {table} where emailid='{id}'"
        cmd.execute(q)
        count=cmd.rowcount
        db.close()
        if(count==0):
            return False,-1
        else:
            result=cmd.fetchone()
            res=bcrypt.checkpw(password,str(result[1]).encode())
            if(res):
                return True,result[0]
            else:
                return False,-1
    except Exception as e:
        print("Error dataBase"+str(e))
        return False,0
def FetchData(id,table):
    try:
        if(table=="student"):
            l=['studentid', 'name', 'address', 'mobile', 'emailid', 'picture', 'previousyearpercentage', 'branch', 'semester', 'numberofbacklog', 'attendencecurrent','clubmember']
        else:
            l=['facultyid', 'facultyname', 'facultycontact', 'emailid', 'picture', 'address', 'stream', 'experience', 'pastexperience', 'clubmember']
        q=f"select * from {table} where {table}id={id}"
        db,cmd=createConnection()
        cmd.execute(q)
        data=cmd.fetchall()
        data=dict(zip(l,data))
        db.close()
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
            q = f"select p.*,s.* from club s,collegeclub p where s.memberid={id} and s.memberstatus={status} and s.clubcode=p.clubid"
            cmd.execute(q)
            dataClub = cmd.fetchall()
            dataClub = dict(zip(l, dataClub))
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
        q = f"update alerts set status={1},permmision={0} where alertid={id}"
        cmd.execute(q)
        db.close()
        return True
    except Exception as e:
        print(e)
        return False