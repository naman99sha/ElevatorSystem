from django.shortcuts import render
from .models import FloorModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from django.contrib.auth.models import User
from rest_framework import status
from elevator.models import ElevatorModel
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
def nextDestinationForElevator(elevator):
    print(elevator.requestList.all().order_by("floorNumber")[0])
    nextDestinationFloor = elevator.requestList.all().order_by("floorNumber")[0]
    if nextDestinationFloor.floorNumber < elevator.currentFloor.floorNumber:
        return True
    else:
        return False

def assignOptimalElevator(floor):
    elevatorList = ElevatorModel.objects.filter(status=True,moving=True)
    minDistance = 0
    assignedElevator = None
    for elevator in elevatorList:
        if elevator.currentFloor != None and elevator.requestList.all() != []:
            if elevator.currentFloor == floor:
                return elevator
            else:
                isElevatorGoingDown = nextDestinationForElevator(elevator)
                if isElevatorGoingDown:
                    if elevator.currentFloor.floorNumber > floor.floorNumber:        
                        if minDistance >= abs(elevator.currentFloor.floorNumber - floor.floorNumber):
                            minDistance = abs(elevator.currentFloor.floorNumber - floor.floorNumber)
                            assignedElevator = elevator
                else:
                    if elevator.currentFloor.floorNumber < floor.floorNumber:        
                        if minDistance >= abs(elevator.currentFloor.floorNumber - floor.floorNumber):
                            minDistance = abs(elevator.currentFloor.floorNumber - floor.floorNumber)
                            assignedElevator = elevator
        elif elevator.currentFloor != None and elevator.requestList.all() == []:
            if minDistance >= abs(elevator.currentFloor.floorNumber - floor.floorNumber):
                minDistance = abs(elevator.currentFloor.floorNumber - floor.floorNumber)
                assignedElevator = elevator
        elif elevator.currentFloor == None and elevator.requestList.all() != []:
            if minDistance >= floor.floorNumber:
                minDistance = floor.floorNumber
                assignedElevator = elevator
        else:
            if minDistance >= floor.floorNumber:
                minDistance = floor.floorNumber
                assignedElevator = elevator
    return assignedElevator


@api_view(['GET'])
def requestElevator(request,floorNumber):
    try:
        floor = FloorModel.objects.get(floorNumber=floorNumber)
        if not request.query_params.get("destination") == None:
            destination = request.query_params.get("destination")
            try:
                destinationFloor = FloorModel.objects.get(floorNumber = int(destination))
            except:
                return Response({"message":f"Given destination of floor {destination} does not exist in the database"},status=status.HTTP_400_BAD_REQUEST)
            elevatorAssigned = assignOptimalElevator(floor)
            if elevatorAssigned != None:
                elevatorAssigned.requestList.add(floor)
                elevatorAssigned.requestList.add(destinationFloor)
                elevatorAssigned.save()
                return Response({"message":f"Elevator {elevatorAssigned.label} coming to floor {floor.floorNumber}"},status=status.HTTP_200_OK)
            else:
                if ElevatorModel.objects.count() == 0:
                    return Response({"message":"0 elevators present in the building"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    elevatorAssigned = ElevatorModel.objects.all().order_by("id").first()
                    elevatorAssigned.requestList.add(floor)
                    elevatorAssigned.requestList.add(destinationFloor)
                    elevatorAssigned.save()
                    return Response({"message":f"Elevator {elevatorAssigned.label} coming to floor {floor.floorNumber}"},status=status.HTTP_200_OK)  

        else:
            return Response({"message":f"No destination passed in the query parameters. Please pass a destination parameter under the key 'destination'"},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message":f"Floor {floorNumber} does not exist in the database"},status=status.HTTP_400_BAD_REQUEST)
