from rest_framework import serializers
from .models import adminUser

class adminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = adminUser
        fields = "__all__"