from django.shortcuts import render
from .models import FloorModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from django.contrib.auth.models import User
from rest_framework import status
# Create your views here.
@api_view(['POST'])
def createFloors(request):
    if request.method == "POST":
        try:
            encoded = request.headers.get('Authorization')
            if encoded.split(" ")[0] != 'Basic':
                return Response({"message":"Needs Basic Authorisation Headers, This action is open for admins only"},status=status.HTTP_401_UNAUTHORIZED)
            encoded = encoded.split(" ")[1]
            username, password = base64.b64decode(encoded).decode('utf-8').split(":")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"message":"User doesn't exist"},status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                return Response({"message":"Wrong Password"},status=status.HTTP_401_UNAUTHORIZED)
            numberOfFloors = request.data.get("NumberOfFloors")
            if numberOfFloors == None:
                return Response({"message":"No input shared, please share the number of floors you wish to register under the key 'NumberOfFloors'"},status=status.HTTP_401_UNAUTHORIZED)
            currentFloorCount = FloorModel.objects.count()
            for i in range(1,numberOfFloors+1):
                obj = FloorModel.objects.create(floorNumber=currentFloorCount+i)
                obj.save()
            return Response({"message":f"{numberOfFloors} floors created successfully by {username}"},status=status.HTTP_201_CREATED)

        except:
            return Response({"message":"Needs Basic Authorisation Headers, This action is open for admins only"},status=status.HTTP_401_UNAUTHORIZED)
        
# API For requesting a lift