from django.urls import path
from . import views
urlpatterns = [
    path('iiitbhopal/gen/1/o/generatealert/<str:token>',views.generateAlert),
]