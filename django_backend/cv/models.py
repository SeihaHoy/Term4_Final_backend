from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class CV(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/cv")  # Provide a default value
    image_pred = models.ImageField(upload_to="images/cv")  # Provide a default value
    text = ArrayField(models.TextField(blank=True, default=''), blank=True, default=list)  # First array of strings
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the record was last updated

    def __str__(self):
        return f"CV object {self.id} - {self.text[:20]}"  # Just showing the first 20 characters of the text for clarity   

# Create your models here.
