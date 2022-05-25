from django.db import models
from django.conf import settings
# Create your models here.

class Account(models.Model):
    display_picture = models.ImageField(null=True, blank=True, editable=True, upload_to="images/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default="")
    department =  models.CharField(max_length=64, default="")
    username = models.CharField(max_length=64, default="")


class Claim(models.Model):
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE)
    claimed = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    practice = models.IntegerField()
    member = models.IntegerField(default=0)
    description = models.CharField(max_length=50)
    tariff = models.IntegerField()
    approval = models.CharField(max_length=50)
    confidence = models.FloatField(blank=True, null=True)
    trees = models.CharField(max_length=50)
    forest = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated_at',)

