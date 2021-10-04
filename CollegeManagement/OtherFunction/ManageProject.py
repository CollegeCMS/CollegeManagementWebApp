import os
from random import sample
from ..SecretKeys.codes import codes
import bcrypt
import uuid
from ..settings import BASE_DIR
def removePic(path=""):
    try:
        os.remove(f"{BASE_DIR}/asserts/user_uploaded_files/{path}")
    except Exception as e:
        print(e)
def passwordGenerate():
    try:
        passGen = "".join(sample(codes['passList'], k=12))
        secretString = codes['Secret-String']
        password = passGen + secretString
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return password,passGen
    except Exception as e:
        print(e)
def fileUniqueId(extention="",file=""):
    try:
        if(extention=="" and file!=""): extention=str(file.name)[str(file.name).rfind('.'):]
        id=str(uuid.uuid4())+extention
        return id
    except Exception as e:
        print(e)
def uploadFile(chunks="",path=""):
    try:
        f=open(f"{BASE_DIR}/asserts/user_uploaded_files/{path}",'wb')
        for chunk in chunks:
            f.write(chunk)
        f.close()
        return True
    except Exception as e:
        print(e)
        return False