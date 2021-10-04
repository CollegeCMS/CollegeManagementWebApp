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
            date=datetime.datetime.strptime(user_data['loginDate'])
            if(date>datetime.date.replace(date.year,date.month,date.day+1)):
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
        raise Exception("Invalid User")
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
                user_data={"userid":res[1],"ip":ip,"loginDate":datetime.datetime.now(),"table":user}
                token=jwt.encode(user_data,codes['secret_key'])
                data[ip]=token
                return redirect(f'/user/dashboard/{token}')
            else:
                if(res[1]==0):
                    return render(request,"error500.html")
                else:
                    return loginPageRender(request,user,"Invalid Credential Please Try Again....")
        else:
            return render(request,"error401.html")
    except Exception as e:
        print("Error controller"+str(e))
        return render(request,"error500.html")
def UserPortal(request,token):
    try:
        res=checkAuth(token,request.META['REMOTE_ADDR'])
        if(res[0]):
            data=fetchData(res[1],res[2])
            if(data[0]):
                return render(request,"userPortal.html",{"data":data[1]})
            else:
                return render(request,"error500.html")
        else:
            if(res[1]==0):
                return redirect("/login")
            elif(res[1]==-1):
                return render(request,"error401.html")
            else:
                return render(request,"error500.html")
    except Exception as e:
        print(e)
        return render(request,"error500.html")

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
                return render(request, "error401.html")
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
                return render(request, "error401.html")
            else:
                return JsonResponse({"status": False})
    except Exception as e:
        print(e)
        return JsonResponse({"status": False})

def checkAuth(token,ip=""):
    try:
        user_data=jwt.decode(token,codes['secret_key'],jwt.get_unverified_header(token)['alg'])
        date = datetime.datetime.strptime(user_data['loginDate'])
        if (date > datetime.date.replace(date.year, date.month, date.day + 1)):
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
