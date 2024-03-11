from django.db import models

# Create your models here.
class adminlocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius= models.FloatField()
    
    def __str__(self) -> str:
        return self.radius
    



