from django.shortcuts import render
from math import radians, sin, cos, sqrt, atan2

# Create your views here.

def attandance(request):
    return render(request,"attandance.html")

def checklocation(request):
    if request.method=="POST":
        lat=float(request.POST.get('lattitude'))
        lon=float(request.POST.get('longitude'))
      
    def haversine_distance(coord1, coord2):
      
        R = 6371000  # meters

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1


        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def is_inside_geofence(employee_location, geofence_center, radius=50):
        
        distance = haversine_distance(employee_location, geofence_center)
        return distance <= radius

    geofence_center = (23.045351984509566, 72.67995464145855)  
    employee_location = (float(lat),float(lon))

    result = is_inside_geofence(employee_location, geofence_center, radius=100) 
    if result:
        message={"mes":"inside the geofancing","latitude":lat,"longitude":lon}
        print("inside+++++++++++")
        return render(request, 'location.html',{"mes":"inside geofensing","latitude":lat,"longitude":lon})
        
    else:
        message={"mes":"outside geofensing","latitude":lat,"longitude":lon}
        print("outside---------")
        return render(request, 'location.html',{"mes":"outside geofensing","latitude":lat,"longitude":lon})