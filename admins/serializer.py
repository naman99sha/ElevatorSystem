from rest_framework import serializers
from .models import adminUser

def checkPasswordValidity(str):
    l, u, p, d = 0, 0, 0, 0
    if (len(str) >= 8):
        for i in str:
            # counting lowercase alphabets
            if (i.islower()):
                l+=1           
        # counting uppercase alphabets
            if (i.isupper()):
                u+=1           
            # counting digits
            if (i.isdigit()):
                d+=1           
            # counting the mentioned special characters
            if(i=='@'or i=='$' or i=='_'):
                    p+=1          
        if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(str)):
            return True
        else:
            return False
    return False

class adminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = adminUser
        fields = ("email","password")
        extra_kwargs = {'password': {'write_only':True}}

    def validate(self, data):
        if not checkPasswordValidity(data['password']):
            raise serializers.ValidationError("Your password should be at least 8 characters long, with at least 1 upper case, 1 lower case, 1 number and 1 special character amongst '@','$' or '_' in it.")
        return super().validate(data)

    def create(self, validated_data):
        user = adminUser.objects.create( email=validated_data['email'], password = validated_data['password'])
        return user