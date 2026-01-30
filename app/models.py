from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Rapport(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    prix = models.PositiveIntegerField()
    probleme = models.TextField()
    contact = models.TextField()