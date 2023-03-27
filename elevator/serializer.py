from .models import ElevatorModel
from rest_framework import serializers

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorModel
        fields = ("label",)