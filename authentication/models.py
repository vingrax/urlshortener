from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length = 10,unique = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)