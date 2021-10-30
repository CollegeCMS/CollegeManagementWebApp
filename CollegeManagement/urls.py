from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.views.static import serve
from . import errors

urlpatterns = [
    url(r'^collegemanagement/iiitbhopal/static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('authentication/',include('authentication.urls')),
    path('event/',include('eventManagement.urls')),
    path('attendance/',include('attendanceManagement.urls')),
    path('',include('adminManagement.urls')),
]
handler404= errors.render404ErrorPage
handler500= errors.render500ErrorPage
