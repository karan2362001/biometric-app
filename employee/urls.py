from django.urls import path
from . import views

urlpatterns = [

    path('/attandance',views.attandance,name="attandance"),
    path('/attandance/checklocation',views.checklocation,name="checklocation")
]