from django.urls import path
from . import views

urlpatterns = [

    path('setlocation/',views.setlocation,name="setlocation"),
    path('getlocation/',views.getlocation,name="getlocation"),
]