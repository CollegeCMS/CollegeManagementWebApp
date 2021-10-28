from django.shortcuts import redirect
from django.http import JsonResponse
from . import eventModel
from authentication.views import checkAuth
import datetime
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
            res=eventModel.saveAlert(data['message'],data['memberid'],str(datetime.datetime.now()),permission,status,data['memberstatus'])
            return JsonResponse({"status":res})
        else:
            if (res[1] == 0):
                return redirect("/authentication/login")
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
            res=eventModel.givePermission(data['alertid'])
            return JsonResponse({"status": res})
        else:
            if (res[1] == 0):
                return redirect("/authentication/login")
            elif (res[1] == -1):
                return JsonResponse({"msg":"Invalid Authentication"},status=401)
            else:
                return JsonResponse({"status": False})
    except Exception as e:
        print(e)
        return JsonResponse({"status": False})

