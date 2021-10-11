import pandas as pd
from functools import reduce
from dateutil.parser import parse
def Computation(a,b):
    sec1=a.second
    sec2=b.second
    min1=a.minute
    min2=b.minute
    hour1=a.hour
    hour2=b.hour
    if(sec1>sec2):
        min2-=1
        sec=60+sec2-sec1
    else:
        sec=sec2-sec1
    if (min1 > min2):
        hour2 -= 1
        min = 60 + min2 - min1
    else:
        min = min2 - min1
    hour=hour2-hour1
    return a.replace(hour,min,sec)
def Computation1(a,b):
    sec=abs(a.second+b.second)
    min=abs(a.minute+b.minute+sec//60)
    sec=sec%60
    hour=abs(a.hour+b.hour+min//60)
    min=min%60
    return a.replace(hour,min,sec)
def manageTimeStamp(name,data):
    left = (data[(data["Full Name"] == name) & (data["User Action"] == "Left")]["Timestamp"])
    join = (data[(data["Full Name"] == name) & (data["User Action"] == "Joined")]["Timestamp"])
    if (len(left) != len(join)):
        left = list(left)
        left.append(parse(f"{12}:{00}:{00}").timetz())
    data = map(Computation, join, left)
    data = list(data)
    data = reduce(Computation1, data)
    return data
data=pd.read_csv('F:/Django Major Project/College Management/CollegeManagement/publicFiles/userUploadedFiles/attendenceFiles/d23c6c63-69f6-43ec-8f2e-7411521ef063.csv',sep="\t")
print(data)
data['Timestamp']=[parse(data['Timestamp'][i]).timetz() for i in range(0,len(data["Timestamp"]))]
names=list(set(data["Full Name"]))
data=pd.DataFrame({"Full Name":names,"Time":[manageTimeStamp(name,data) for name in names]})
print(data)