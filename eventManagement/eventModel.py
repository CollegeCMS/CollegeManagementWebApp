from CollegeManagement.connection import createConnection
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