from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


# class NLP(models.Model):
#     id = models.AutoField(primary_key=True)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
class NLP(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()  # This will store the raw text
    array_1 = ArrayField(models.CharField(max_length=255), blank=True, default=list)  # First array of strings
    array_2 = ArrayField(models.CharField(max_length=255), blank=True, default=list)  # Second array of strings
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the record was last updated

    def __str__(self):
        return f"NLP object {self.id} - {self.text[:20]}"  # Just showing the first 20 characters of the text for clarity
    
class CV(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/", default='default.jpg')  # Provide a default value
    image_pred = models.ImageField(upload_to="images/pred/", default='default_pred.jpg')  # Provide a default value
    text = ArrayField(models.CharField(max_length=255), blank=True, default=list)  # First array of strings
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the record was last updated

    def __str__(self):
        return f"CV object {self.id} - {self.text[:20]}"  # Just showing the first 20 characters of the text for clarity   
