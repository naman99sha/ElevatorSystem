from django.shortcuts import render
from .models import ElevatorModel
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import ElevatorSerializer
import base64
# Create your views here.
class CreateElevator(generics.GenericAPIView):
    serializer_class = ElevatorSerializer

    def post(self, request, *args, **kwargs):
        try:
            encoded = request.headers.get('Authorization')
            if encoded.split(" ")[0] != 'Basic':
                return Response({"message":"Needs Basic Authorisation Headers, This action is open for admins only 1"},status=status.HTTP_401_UNAUTHORIZED)
            encoded = encoded.split(" ")[1]
            username, password = base64.b64decode(encoded).decode('utf-8').split(":")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"message":"User doesn't exist"},status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                return Response({"message":"Wrong Password"},status=status.HTTP_401_UNAUTHORIZED)
            numberOfElevators = request.data.get("n")
            if numberOfElevators == None:
                return Response({"message":"No input shared, please share the number of Elevators you wish to register under the key 'n'"},status=status.HTTP_401_UNAUTHORIZED)
            currentElevatorCount = ElevatorModel.objects.count()
            for i in range(1,abs(currentElevatorCount-numberOfElevators)+1):
                serializer = self.get_serializer(data={"label":f"{i}"})
                serializer.is_valid(raise_exception=True)
                elevator = serializer.save()
            return Response({"message":f"{numberOfElevators} Elevators created successfully by {username}"},status=status.HTTP_201_CREATED)
        except:
            return Response({"message":"Needs Basic Authorisation Headers, This action is open for admins only 2"},status=status.HTTP_401_UNAUTHORIZED)