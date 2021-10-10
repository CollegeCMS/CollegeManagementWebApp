from django.shortcuts import render,redirect
from ..models import Authentication
from django.http import JsonResponse
import datetime
from ..SecretKeys.codes import codes
import jwt
data={}
def preLoginPageRender(request):
    try:
        ip=request.META.get("REMOTE_ADDR")
        if(ip in data):
            user_data=jwt.decode(data[ip],codes['secret_key'],jwt.get_unverified_header(data[ip])['alg'])
            date=datetime.datetime.fromisoformat(user_data['loginDate'])
            date = date.toordinal() - datetime.datetime.now().toordinal()
            if(date>1):
                data.pop(ip)
                return render(request, "preLogin.html")
            else:
                return redirect(f'/user/dashboard/{data[ip]}')
        else:
            return render(request,"preLogin.html")
    except jwt.DecodeError as e:
        return render(request,"error401.html")
    except Exception as e:
        return render(request,"error500.html")
def loginPageRender(request,user="",msg=""):
    try:
        print(user,request.META['REQUEST_METHOD'])
        if(user=="faculty" or user=="student"):
            return render(request,"loginPage.html",{"user":user,"msg":msg})
        else:
            return redirect('/login')
    except Exception as e:
        print(e)
        return render(request,"error500.html")

def Login(request,user):
    try:
        if(request.META['REQUEST_METHOD']=="GET"):
            return render(request,"error404.html")
        ip = request.META.get("REMOTE_ADDR")
        if(user=="faculty" or user=="student"):
            res=Authentication.checkCredential(request.POST['id'],request.POST['password'],user)
            if(res[0]):
                user_data={"userid":res[1],"ip":ip,"loginDate":str(datetime.datetime.now()),"table":user}
                token=jwt.encode(user_data,codes['secret_key'])
                data[ip]=token
                return redirect(f'/user/dashboard/{token}')
            else:
                if(res[1]==0):
                    return JsonResponse({"msg":"Server Error"},status=500)
                else:
                    return loginPageRender(request,user,"Invalid Credential Please Try Again....")
        else:
            return render(request,"error401.html")
    except Exception as e:
        print("Error controller"+str(e))
        return JsonResponse({"msg":"Server Error"},status=500)
def UserPortal(request,token):
    try:
        res=checkAuth(token,request.META['REMOTE_ADDR'])
        if(res[0]):
            data=fetchData(res[1],res[2])
            if(data[0]):
                return render(request,"userPortal.html",{"data":data[1],'token':token})
            else:
                return JsonResponse({"msg":"Server Error"},status=500)
        else:
            if(res[1]==0):
                return redirect("/login")
            elif(res[1]==-1):
                return render(request,"error401.html")
            else:
                return JsonResponse({"msg":"Server Error"},status=500)
    except Exception as e:
        print(e)
        return JsonResponse({"msg":"Server Error"},status=500)

def LogOut(request,token):
    try:
        ip=request.META['REMOTE_ADDR']
        res=checkAuth(token,ip)
        if (res[0]):
            data.pop(ip)
            return redirect('/login')
        else:
            if (res[1] == 0):
                return redirect(f'/user/dashboard/{token}')
            elif (res[1] == -1):
                return render(request, "error401.html")
            else:
                return JsonResponse({"msg": "Server Error"}, status=500)
    except Exception as e:
        print(e)
        return JsonResponse({"msg": "Server Error"}, status=500)

def generateAlert(request,token):
    try:
        data=request.POST
        ip=request.META['REMOTE_ADDR']
        res=checkAuth(token,ip)
        if(res[0]):
            if(data['memberstatus']=="student"):
                permission=1
                status=0
            else:
                permission=0
                status=1
            res=Authentication.saveAlert(data['message'],data['memberid'],str(datetime.datetime.now()),permission,status,data['memberstatus'])
            return JsonResponse({"status":res})
        else:
            if (res[1] == 0):
                return redirect("/login")
            elif (res[1] == -1):
                return JsonResponse({"msg":"Invalid Authentication"},status=401)
            else:
                return JsonResponse({"status":False})
    except Exception as e:
        print(e)
        return JsonResponse({"status":False})

def givePermission(request,token):
    try:
        data = request.GET
        ip = request.META['REMOTE_ADDR']
        res = checkAuth(token, ip)
        if (res[0]):
            res=Authentication.givePermission(data['alertid'])
            return JsonResponse({"status": res})
        else:
            if (res[1] == 0):
                return redirect("/login")
            elif (res[1] == -1):
                return JsonResponse({"msg":"Invalid Authentication"},status=401)
            else:
                return JsonResponse({"status": False})
    except Exception as e:
        print(e)
        return JsonResponse({"status": False})

def checkAuth(token,ip=""):
    try:
        if(ip not in data):
            return False,0
        user_data=jwt.decode(token,codes['secret_key'],jwt.get_unverified_header(token)['alg'])
        date = datetime.datetime.fromisoformat(user_data['loginDate'])
        date=date.toordinal()-datetime.datetime.now().toordinal()
        print(date)
        if (date > 1):
            data.pop(user_data['ip'])
            return False, 0

        else:
            if(user_data['ip']==ip):
                return True,user_data['userid'],user_data['table']
            else:
                return False,-1
    except jwt.DecodeError as e:
        print(e)
        return False,-1
    except Exception as e:
        print(e)
        return False,1

def fetchData(id,table):
    try:
        data=Authentication.FetchData(id,table)
        return data
    except Exception as e:
        print(e)
        return False,""
def handleServerError(request):
    try:
        return render(request,"error500.html")
    except Exception as e:
        print(e)
        raise Exception("error")
def manageCSV(file):
    f=open(file,"r")
    data=f.read()[2:].replace("\x00","")
    f.close()
    f=open(file,"w")
    f.write(data)
    f.close()
def uploadAttendenceFile(request,token):
    pass
