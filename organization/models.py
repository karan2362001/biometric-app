from django.db import models
from account.models import User

# Create your models here.
class Organization(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200)
    contact_number=models.BigIntegerField(null=True,blank=True)
    address=models.TextField()
    logo=models.ImageField(upload_to='admin/logo')
    password=models.CharField(max_length=200)
    
    def __str__(self):
        return self.company_name
    