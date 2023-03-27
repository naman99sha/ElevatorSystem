from django.shortcuts import render
from .models import ElevatorModel
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import ElevatorSerializer
import base64
# Create your views here.
def checkForAuthentication(encoded):
    try:
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
        return user
    except:
        return Response({"message":"Needs Basic Authorisation Headers, This action is open for admins only"},status=status.HTTP_401_UNAUTHORIZED)

class CreateElevator(generics.GenericAPIView):
    serializer_class = ElevatorSerializer

    def post(self, request, *args, **kwargs):

        encoded = request.headers.get('Authorization')
        temp = checkForAuthentication(encoded)
        try:
            if temp.username:
                user = temp
        except AttributeError: return temp
        numberOfElevators = request.data.get("n")
        if numberOfElevators == None:
            return Response({"message":"No input shared, please share the number of Elevators you wish to register under the key 'n'"},status=status.HTTP_401_UNAUTHORIZED)
        currentElevatorCount = ElevatorModel.objects.count()
        for i in range(1,numberOfElevators+1):
            serializer = self.get_serializer(data={"label":f"{currentElevatorCount+i}"})
            serializer.is_valid(raise_exception=True)
            elevator = serializer.save()
        return Response({"message":f"{numberOfElevators} Elevators created successfully by {user.username}"},status=status.HTTP_201_CREATED)


class RequestListElevator(generics.GenericAPIView):

    def get(self, request, label, *args, **kwargs):
        encoded = request.headers.get('Authorization')
        temp = checkForAuthentication(encoded)
        try:
            if temp.username:
                user = temp
        except AttributeError: return temp
        try:
            elevator = ElevatorModel.objects.get(label=label)
            temp = []
            for i in elevator.requestList.all():
                temp.append(f"Floor Number {i.floorNumber}")
            return Response({"Request-List":temp},status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)