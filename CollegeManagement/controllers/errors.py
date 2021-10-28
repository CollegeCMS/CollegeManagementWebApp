from django.shortcuts import render
def render404ErrorPage(request,exception):
    return render(request,"error404.html")
def render500ErrorPage(request):
    return render(request,"error500.html")
# import os.path
# from ..models import Authentication
# from django.http import JsonResponse
# import datetime
# from ..settings import BASE_DIR
# from ..OtherFunction import ManageProject
# from authentication.views import checkAuth,fetchData
# import threading
# from ..SecretKeys.codes import codes
# import pandas as pd
# from functools import reduce
# from dateutil.parser import parse
# from ..models.connection import createDataConnection
# import jwt
# data={}
# def preLoginPageRender(request):
#     try:
#         ip=request.META.get("REMOTE_ADDR")
#         if(ip in data):
#             user_data=jwt.decode(data[ip],codes['secret_key'],jwt.get_unverified_header(data[ip])['alg'])
#             date=datetime.datetime.fromisoformat(user_data['loginDate'])
#             date = date.toordinal() - datetime.datetime.now().toordinal()
#             if(date>1):
#                 data.pop(ip)
#                 return render(request, "preLogin.html")
#             else:
#                 return redirect(f'/user/dashboard/{data[ip]}')
#         else:
#             return render(request,"preLogin.html")
#     except jwt.DecodeError as e:
#         return render(request,"error401.html")
#     except Exception as e:
#         return render(request,"error500.html")
# def loginPageRender(request,user="",msg=""):
#     try:
#         if(user=="faculty" or user=="student"):
#             return render(request,"loginPage.html",{"user":user,"msg":msg})
#         else:
#             return redirect('/login')
#     except Exception as e:
#         print(e)
#         return render(request,"error500.html")
#
# def Login(request,user):
#     try:
#         if(request.META['REQUEST_METHOD']=="GET"):
#             return render(request,"error404.html")
#         ip = request.META.get("REMOTE_ADDR")
#         if(user=="faculty" or user=="student"):
#             res=Authentication.checkCredential(request.POST['id'],request.POST['password'],user)
#             if(res[0]):
#                 user_data={"userid":res[1],"ip":ip,"loginDate":str(datetime.datetime.now()),"table":user}
#                 token=jwt.encode(user_data,codes['secret_key'])
#                 data[ip]=token
#                 return redirect(f'/user/dashboard/{token}')
#             else:
#                 if(res[1]==0):
#                     return JsonResponse({"msg":"Server Error"},status=500)
#                 else:
#                     return loginPageRender(request,user,"Invalid Credential Please Try Again....")
#         else:
#             return render(request,"error401.html")
#     except Exception as e:
#         print("Error controller"+str(e))
#         return JsonResponse({"msg":"Server Error"},status=500)
# def LogOut(request,token):
#     try:
#         ip=request.META['REMOTE_ADDR']
#         res=checkAuth(token,ip)
#         if (res[0]):
#             data.pop(ip)
#             return redirect('/login')
#         else:
#             if (res[1] == 0):
#                 return redirect(f'/user/dashboard/{token}')
#             elif (res[1] == -1):
#                 return render(request, "error401.html")
#             else:
#                 return JsonResponse({"msg": "Server Error"}, status=500)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"msg": "Server Error"}, status=500)

# def UserPortal(request,token):
#     try:
#         res=checkAuth(token,request.META['REMOTE_ADDR'])
#         if(res[0]):
#             data=fetchData(res[1],res[2])
#             if(data[0]):
#                 return render(request,"userPortal.html",{"data":data[1],'token':token})
#             else:
#                 return JsonResponse({"msg":"Server Error"},status=500)
#         else:
#             if(res[1]==0):
#                 return redirect("/login")
#             elif(res[1]==-1):
#                 return render(request,"error401.html")
#             else:
#                 return JsonResponse({"msg":"Server Error"},status=500)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"msg":"Server Error"},status=500)
#

# def generateAlert(request,token):
#     try:
#         data=request.POST
#         ip=request.META['REMOTE_ADDR']
#         res=checkAuth(token,ip)
#         if(res[0]):
#             if(data['memberstatus']=="student"):
#                 permission=1
#                 status=0
#             else:
#                 permission=0
#                 status=1
#             res=Authentication.saveAlert(data['message'],data['memberid'],str(datetime.datetime.now()),permission,status,data['memberstatus'])
#             return JsonResponse({"status":res})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg":"Invalid Authentication"},status=401)
#             else:
#                 return JsonResponse({"status":False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"status":False})
#
# def givePermission(request,token):
#     try:
#         data = request.GET
#         ip = request.META['REMOTE_ADDR']
#         res = checkAuth(token, ip)
#         if (res[0]):
#             res=Authentication.givePermission(data['alertid'])
#             return JsonResponse({"status": res})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg":"Invalid Authentication"},status=401)
#             else:
#                 return JsonResponse({"status": False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"status": False})

# def checkAuth(token,ip=""):
#     try:
#         if(ip not in data):
#             return False,0
#         user_data=jwt.decode(token,codes['secret_key'],jwt.get_unverified_header(token)['alg'])
#         date = datetime.datetime.fromisoformat(user_data['loginDate'])
#         date=date.toordinal()-datetime.datetime.now().toordinal()
#         if (date > 1):
#             data.pop(user_data['ip'])
#             return False, 0
#
#         else:
#             if(user_data['ip']==ip):
#                 return True,user_data['userid'],user_data['table']
#             else:
#                 return False,-1
#     except jwt.DecodeError as e:
#         print(e)
#         return False,-1
#     except Exception as e:
#         print(e)
#         return False,1
#
# def fetchData(id,table):
#     try:
#         data=Authentication.FetchData(id,table)
#         return data
#     except Exception as e:
#         print(e)
#         return False,""
# def manageCSV(file):
#     f=open(file,"r")
#     data=f.read()[2:].replace("\x00","")
#     f.close()
#     data=data.strip()
#     f=open(file,"w")
#     f.write(data)
#     f.close()
#     p=convertToFrame(file)
#     return p
# def uploadAttenceFile(file,id):
#     try:
#         f=open(f"{BASE_DIR}/publicFiles/userUploadedFiles/attendenceFiles/{id}",'wb')
#         for chunk in file.chunks():
#             f.write(chunk)
#         f.close()
#         p=manageCSV(f"{BASE_DIR}/publicFiles/userUploadedFiles/attendenceFiles/{id}")
#         if(p[0]):
#             return True,p
#         else:
#             return [False]
#     except Exception as e:
#         print(e)
#         return False,0
# def uploadAttendenceFileUrl(request,token):
#     try:
#         ip = request.META['REMOTE_ADDR']
#         res = checkAuth(token, ip)
#         if (res[0]):
#             data = request.POST
#             subjectid=data['subjectid']
#             file = request.FILES['attendencefile']
#             date=data['dateupload']
#             date=datetime.date.fromisoformat(date).toordinal()
#             fileid=ManageProject.fileUniqueId(file=file)
#             res=uploadAttenceFile(file,fileid)
#             if(res[0]):
#                 res=res[1]
#                 manageAttendence=threading.Thread(target=analysis,args=(res[2],subjectid,fileid,date))
#                 manageAttendence.start()
#                 res=Authentication.uploadAttendenceFile(fileid,subjectid,res[1],date)
#                 if(res):
#                     return JsonResponse({"status": True})
#                 else:
#                     return JsonResponse({"status": False})
#             else:
#                 return JsonResponse({"status": False})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg": "Invalid Authentication"}, status=401)
#             else:
#                 return JsonResponse({"status": False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"status": False})
# def Computation(a,b):
#     sec1=a.second
#     sec2=b.second
#     min1=a.minute
#     min2=b.minute
#     hour1=a.hour
#     hour2=b.hour
#     if(sec1>sec2):
#         min2-=1
#         sec=60+sec2-sec1
#     else:
#         sec=sec2-sec1
#     if (min1 > min2):
#         hour2 -= 1
#         min = 60 + min2 - min1
#     else:
#         min = min2 - min1
#     hour=hour2-hour1
#     return a.replace(hour,min,sec)
# def Computation1(a,b):
#     sec=abs(a.second+b.second)
#     min=abs(a.minute+b.minute+sec//60)
#     sec=sec%60
#     hour=abs(a.hour+b.hour+min//60)
#     min=min%60
#     return a.replace(hour,min,sec)
# def manageTimeStamp(name,data):
#     left = (data[(data["Full Name"] == name) & (data["User Action"] == "Left")]["Timestamp"])
#     join = (data[(data["Full Name"] == name) & (data["User Action"] == "Joined")]["Timestamp"])
#     if (len(left) != len(join)):
#         left = list(left)
#         left.append(parse(f"{12}:{00}:{00}").timetz())
#     data = map(Computation, join, left)
#     data = list(data)
#     data = reduce(Computation1, data)
#     return data
# def convertToFrame(file):
#     try:
#         data = pd.read_csv(file, sep="\t")
#         return True,len(set(data['Full Name']))-1,data
#     except Exception as e:
#         print(e)
#         return [False]
# def analysis(data,subjectid,file,date):
#     try:
#         data['Timestamp'] = [parse(data['Timestamp'][i]).timetz() for i in range(0, len(data["Timestamp"]))]
#         names=set(data["Full Name"])
#         res=Authentication.fetchAllStudent(subjectid)
#         data1= pd.DataFrame({"studentid":[item['studentid'] for item in res[1]],"name":[item['name'] for item in res[1]]})
#         data1[['time',f"{datetime.date.fromordinal(date)}"]]=[[manageTimeStamp(name, data),"P"] if(name in names) else [0,"A"] for name in data1['name']]
#         data1['subjectid']=subjectid
#         data1.to_csv(f"{BASE_DIR}/publicFiles/userUploadedFiles/attendenceFiles/{file}",index=False)
#         data1['date']=str(date)
#         engine=createDataConnection()
#         data1=data1.rename({f"{datetime.date.fromordinal(date)}":"attendence"},axis="columns")
#         data1[['studentid',"subjectid","date","attendence"]].to_sql('studentattendence', con=engine, if_exists="append", index=False)
#     except Exception as e:
#         print(e)
# def getAttendence(request,token):
#     try:
#         ip = request.META['REMOTE_ADDR']
#         res = checkAuth(token, ip)
#         if (res[0]):
#             date=request.GET['date']
#             id=request.GET['subjectid']
#             date=datetime.date.fromisoformat(date).toordinal()
#             data=Authentication.getAttendence(id,date)
#             if(data[0]):
#                 data[2] = list(zip(*data[2]))
#                 data[2] = dict(zip(["Student Id", "Name", "Present", "Absent"], data[2]))
#                 generateAnalysisFile(data[2],data[1]['filename'])
#                 return JsonResponse({"data":data[1],"analysis":data[2]})
#             else:
#                 return JsonResponse({"data":{}})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg": "Invalid Authentication"}, status=401)
#             else:
#                 return JsonResponse({"status": False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"data":{}})
# def generateAnalysisFile(res,filename):
#     try:
#         res=pd.DataFrame(res)
#         res['Total Days']=res['Present']+res['Absent']
#         res['Percentage']=res['Present']*100/res["Total Days"]
#         res.to_csv(f"{BASE_DIR}/publicFiles/userUploadedFiles/attendenceFiles/analysis{filename}",index=False)
#     except Exception as e:
#         print(e)
# def getSubjectid(request,token):
#     try:
#         ip = request.META['REMOTE_ADDR']
#         res = checkAuth(token, ip)
#         if (res[0]):
#             id=res[1]
#             data=Authentication.getsubjectid(id)
#             if(data[0]):
#                 return JsonResponse({'data':data[1]})
#             else:
#                 return JsonResponse({"data":[]})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg": "Invalid Authentication"}, status=401)
#             else:
#                 return JsonResponse({"status": False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"data":[]})
# def uploadAttendencePage(request,token):
#     try:
#         ip = request.META['REMOTE_ADDR']
#         res = checkAuth(token, ip)
#         if (res[0]):
#             return render(request,"uploadAttendence.html",{"token":token})
#         else:
#             if (res[1] == 0):
#                 return redirect("/login")
#             elif (res[1] == -1):
#                 return JsonResponse({"msg": "Invalid Authentication"}, status=401)
#             else:
#                 return JsonResponse({"status": False})
#     except Exception as e:
#         print(e)
#         return JsonResponse({"data":{}})
        
