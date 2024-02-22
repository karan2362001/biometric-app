from django.db import models

# Create your models here.
# models.py
import face_recognition

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    face_encoding = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            # Compute face encoding when an image is uploaded
            image_path = self.image.path
            face_encodings = []
            try:
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
            except Exception as e:
                print(f"Error processing image: {e}")
            
            # Save the face encoding to the model instance
            if face_encodings:
                self.face_encoding = face_encodings[0].tolist()  # Save the first face encoding as JSON string
        
        super().save(*args, **kwargs)
