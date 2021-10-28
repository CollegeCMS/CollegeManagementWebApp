from django.urls import path
from . import  views
urlpatterns = [
    path('uploadfile/<str:token>',views.uploadAttendenceFileUrl),
    path('getattendence/<str:token>/',views.getAttendence),
    path('uploadattendence/gen/o/u/<str:token>/',views.uploadAttendencePage),
]