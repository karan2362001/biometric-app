from django.shortcuts import render
from geofence.models import adminlocation
from .models import  adminlocation


# Create your views here.
def setlocation(request):
     return render(request,"geof.html")


def getlocation(request):
    if request.method=="POST":
        lat=float(request.POST.get('lattitude'))
        lon=float(request.POST.get('longitude'))
        range1=float(request.POST.get('rangeSlider'))
        locations=adminlocation.objects.create(latitude = lat, longitude = lon ,radius=range1)
        locations.save()
    
   
    return render(request, 'adminlocation.html',{"lattitude":lat,"longitude":lon,"range":range1})
 
 