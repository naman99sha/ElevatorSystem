from django.db import models

# Create your models here.
class FloorModel(models.Model):
    floorNumber = models.BigIntegerField(null=True,unique=True)

    def __str__(self) -> str:
        return f"Floor Number {self.floorNumber}"
