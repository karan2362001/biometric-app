from django.db import models
from account.models import User
from organization.models import Organization
import face_recognition
import json

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employee')
    timing = models.CharField(max_length=50)
    face_encoding = models.JSONField(blank=True, null=True)  # Changed to JSONField for storing arrays
    mobile_number = models.BigIntegerField(null=True, blank=True)
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
  

    def __str__(self):
        if self.photo:
            # Compute face encoding when an image is uploaded
            image_path = self.photo.path
            try:
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    # Save face encodings as JSON
                    self.face_encoding = json.dumps(face_encodings[0].tolist())
            except Exception as e:
                print(f"Error processing image: {e}")
                # Handle error gracefully, log or notify user as needed
        
        super().save()
        return self.user.username