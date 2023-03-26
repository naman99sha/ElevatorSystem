from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class adminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return f"Admin User {self.username}"
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email
            userObj = User.objects.create_user(self.username, self.email, self.password)
            self.user = userObj
        return super(adminUser, self).save(*args, **kwargs)