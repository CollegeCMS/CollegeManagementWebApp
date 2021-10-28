from django.shortcuts import render,redirect
from django.http import JsonResponse
from . import adminModal
from authentication.views import checkAuth,fetchData
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
                return redirect("/authentication/login")
            elif(res[1]==-1):
                return render(request,"error401.html")
            else:
                return JsonResponse({"msg":"Server Error"},status=500)
    except Exception as e:
        print(e)
        return JsonResponse({"msg":"Server Error"},status=500)

def getSubjectid(request,token):
    try:
        ip = request.META['REMOTE_ADDR']
        res = checkAuth(token, ip)
        if (res[0]):
            id=res[1]
            data=adminModal.getsubjectid(id)
            if(data[0]):
                return JsonResponse({'data':data[1]})
            else:
                return JsonResponse({"data":[]})
        else:
            if (res[1] == 0):
                return redirect("/authentication/login")
            elif (res[1] == -1):
                return JsonResponse({"msg": "Invalid Authentication"}, status=401)
            else:
                return JsonResponse({"status": False})
    except Exception as e:
        print(e)
        return JsonResponse({"data":[]})
