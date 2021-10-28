from django.urls import path
from . import views
urlpatterns=[
    path('login/', views.preLoginPageRender),
    path(r'auth/o/log/login/<str:user>/',views.loginPageRender),
    path('auth/o/1/log/college/Login/<str:user>',views.Login),
    path('user/o/logout/<str:token>/', views.LogOut),
]