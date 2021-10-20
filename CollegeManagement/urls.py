from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from .controllers import Login
from django.shortcuts import render
def render404ErrorPage(request,exception):
    return render(request,"error404.html")
urlpatterns = [
    url(r'^collegemanagement/iiitbhopal/static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('login/', Login.preLoginPageRender),
    path(r'auth/o/log/login/<str:user>/',Login.loginPageRender),
    path('auth/o/1/log/college/Login/<str:user>',Login.Login),
    path('user/dashboard/<str:token>/',Login.UserPortal),
    path('iiitbhopal/gen/1/o/generatealert/<str:token>',Login.generateAlert),
    path('user/o/logout/<str:token>/',Login.LogOut),
    path('uploadfile/<str:token>',Login.uploadAttendenceFileUrl),
    path('getattendence/<str:token>/',Login.getAttendence),
    path('getsubjectid/<str:token>/',Login.getSubjectid),
    path('uploadattendence/gen/o/u/<str:token>/',Login.uploadAttendencePage),
]
handler404=render404ErrorPage
handler500=Login.handleServerError
