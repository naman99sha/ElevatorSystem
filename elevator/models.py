from django.db import models
from floor.models import FloorModel
# Create your models here.
class ElevatorModel(models.Model):
    label = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    currentFloor = models.ForeignKey(FloorModel, on_delete=models.SET_NULL, related_name="currentFloorFloorModel",null=True)
    moving = models.BooleanField(default=False)
    requestList = models.ManyToManyField(FloorModel,related_name="requestListFloorModel")

    def __str__(self) -> str:
        return f"Lift Number {self.label}"