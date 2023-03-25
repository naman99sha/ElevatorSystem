from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class adminUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=255, null=True,blank=False)

    def __str__(self) -> str:
        return f"Admin User {self.username}"

