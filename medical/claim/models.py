from django.db import models
from django.conf import settings
# Create your models here.

class Account(models.Model):
    display_picture = models.ImageField(null=True, blank=True, editable=True, upload_to="images/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=64)