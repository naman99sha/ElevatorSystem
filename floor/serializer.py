from rest_framework import serializers
from .models import FloorModel

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorModel
        fields = ('floorNumber')