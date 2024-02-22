from django.db import models

# Create your models here.
class adminlocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius= models.FloatField()
    



