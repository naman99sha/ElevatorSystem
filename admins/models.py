from django.db import models

# Create your models here.
class adminUser(models.Model):
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return f"Admin User {self.username}"
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email
        return super(adminUser, self).save(*args, **kwargs)