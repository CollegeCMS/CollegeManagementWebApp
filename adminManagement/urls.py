from django.urls import path
from . import views
urlpatterns = [
    path('user/dashboard/<str:token>/', views.UserPortal),

    path('getsubjectid/<str:token>/', views.getSubjectid),
]