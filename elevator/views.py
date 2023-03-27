from django.shortcuts import render
from .models import ElevatorModel
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import ElevatorSerializer
import base64
from floor.models import FloorModel

# HELPER FUNCTION TO CHECK IF THE USER REQUESTING THE ACTION IS AN ADMIN
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

# TO INITIALIZE ELEVATORS
# ADMIN ONLY
# NEEDS BASIC-AUTH HEADERS
# BODY = {"n":<number of elevators>}
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

# TO GET THE REQUEST LIST OF AN ELEVATOR
# ADMIN ONLY
# NEEDS BASIC AUTH HEADERS
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
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
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            temp = []
            for i in elevator.requestList.all():
                temp.append(f"Floor Number {i.floorNumber}")
            return Response({"Request-List":temp},status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO MARK AN ELEVATOR AS ACTIVE OR UNDER MAINTENANCE
# ADMIN ONLY
# NEEDS BASIC AUTH HEADERS
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class ChangeElevatorStatus(generics.GenericAPIView):
    def post(self, request, label, *args, **kwargs):

        encoded = request.headers.get('Authorization')
        temp = checkForAuthentication(encoded)
        try:
            if temp.username:
                user = temp
        except AttributeError: return temp
        try:
            elevator = ElevatorModel.objects.get(label = label)
            statusVal = request.data.get("status")
            if statusVal == None:
                return Response({"message":f"No input shared, please share the status to be set for the elevator {label} under the key 'status' as true or false"}, status=status.HTTP_400_BAD_REQUEST)
            elevator.status = statusVal
            elevator.save()
            if statusVal:
                return Response({"message":f"Elevator {label} marked as active by {user.username}"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":f"Elevator {label} marked as under maintenance by {user.username}"},status=status.HTTP_201_CREATED)
        except:
            return Response({"message":f"Elevator {label} does not exist"},status=status.HTTP_400_BAD_REQUEST)

# TO GET THE ELEVATOR GO UP A FLOOR
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class ElevatorGoUp(generics.GenericAPIView):

    def post(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.currentFloor == None:
                elevator.currentFloor = FloorModel.objects.get(floorNumber=1)
                elevator.save()
                if elevator.currentFloor in elevator.requestList.all():
                    elevator.requestList.remove(elevator.currentFloor)
                    elevator.save()
            else:
                try:
                    elevator.currentFloor = FloorModel.objects.get(floorNumber=elevator.currentFloor.floorNumber + 1)
                except:
                    return Response({"message":f"Elevator {label} is already on top floor"}, status=status.HTTP_400_BAD_REQUEST)
                elevator.save()
                if elevator.currentFloor in elevator.requestList.all():
                    elevator.requestList.remove(elevator.currentFloor)
                    elevator.save()
            return Response({"message":f"{elevator.label} Elevator went up 1 level to floor {elevator.currentFloor.floorNumber} "}, status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO GET THE ELEVATOR GO DOWN A FLOOR
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class ElevatorGoDown(generics.GenericAPIView):

    def post(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.currentFloor == None:
                return Response({"message":f"Elevator {label} already on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if elevator.currentFloor.floorNumber == 1:
                    elevator.currentFloor = None
                    elevator.save()
                    if elevator.currentFloor in elevator.requestList.all():
                        elevator.requestList.remove(elevator.currentFloor)
                        elevator.save()
                    return Response({"message":f"{elevator.label} Elevator went down 1 level to ground floor"}, status=status.HTTP_200_OK)
                elevator.currentFloor = FloorModel.objects.get(floorNumber=elevator.currentFloor.floorNumber - 1)
                elevator.save()
                if elevator.currentFloor in elevator.requestList.all():
                    elevator.requestList.remove(elevator.currentFloor)
                    elevator.save()
            return Response({"message":f"{elevator.label} Elevator went down 1 level to floor {elevator.currentFloor.floorNumber} "}, status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        

# TO START/STOP AN ELEVATOR
# IF ELEVATOR IS IN START MODE BEFORE, IT WILL STOP AND VICE VERSA
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class ChangeElevatorMoving(generics.GenericAPIView):

    def post(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving:
                elevator.moving = False
                elevator.save()
                return Response({"message":f"Elevator {elevator.label} is stopped"}, status=status.HTTP_200_OK)
            else:
                elevator.moving = True
                elevator.save()
                return Response({"message":f"Elevator {elevator.label} is moving"}, status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO GET THE ELEVATOR'S CURRENT FLOOR
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class GetElevatorCurrentFloor(generics.GenericAPIView):

    def get(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.currentFloor == None:
                return Response({"message":f"Elevator {label} currently at ground floor"})
            else:
                return Response({"message":f"Elevator {label} currently at Floor {elevator.currentFloor.floorNumber}"})
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO OPEN ELEVATOR DOORS
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class OpenElevatorDoor(generics.GenericAPIView):

    def post(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":f"Elevator {label} doors open"})
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO CLOSE ELEVATOR DOORS
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class CloseElevatorDoor(generics.GenericAPIView):

    def post(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":f"Elevator {label} doors closed"})
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# HELPER FUNCTION TO FIND THE NEXT DESTINATION FLOOR FOR AN ELEVATOR OPTIMALLY
def nextDestinationForElevator(elevator):
    nextDestinationFloor = elevator.requestList.all().order_by("floorNumber").first()
    if nextDestinationFloor.floorNumber < elevator.currentFloor.floorNumber:
        if elevator.requestList.filter(floorNumber__lte=nextDestinationFloor.floorNumber).count() > elevator.requestList.filter(floorNumber__gt=nextDestinationFloor.floorNumber):
            return nextDestinationFloor
        else:
            nextDestinationFloor = elevator.requestList.filter(floorNumber__gt=nextDestinationFloor.floorNumber).order_by("floorNumber").first()
            return nextDestinationFloor
    else:
        if elevator.requestList.filter(floorNumber__lte=nextDestinationFloor.floorNumber).count() < elevator.requestList.filter(floorNumber__gt=nextDestinationFloor.floorNumber).count():
            return nextDestinationFloor
        else:
            nextDestinationFloor = elevator.requestList.filter(floorNumber__lte=nextDestinationFloor.floorNumber).order_by("floorNumber").first()
            return nextDestinationFloor
        
# TO RETURN ELEVATOR'S NEXT DESTINATION
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class GetElevatorNextDestination(generics.GenericAPIView):

    def get(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.requestList.all().count() == 0:
                return Response({"message":f"Elevator {label} has no next destination"},status=status.HTTP_200_OK)
            return Response({"message":f"Elevator {label} going to floor {nextDestinationForElevator(elevator).floorNumber} next"},status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
# TO SEE IF AN ELEVATOR IS GOING UP OR DOWN ACCORDING TO IT'S NEXT DESTINATION
# NEEDS THE ELEVATOR LABEL TO ACT AS AN ID 
class ElevatorGoingUpOrDown(generics.GenericAPIView):

    def get(self, request, label, *args, **kwargs):
        try:
            elevator = ElevatorModel.objects.get(label=label)
            if elevator.status == False:
                return Response({"message":f"Elevator {label} under maintenance"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.moving == False:
                if elevator.currentFloor != None:
                    return Response({"message":f"Elevator {label} stopped on floor {elevator.currentFloor.floorNumber}"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":f"Elevator {label} stopped on ground floor"},status=status.HTTP_400_BAD_REQUEST)
            if elevator.requestList.all().count() == 0:
                return Response({"message":f"Elevator {label} isn't going anywhere"},status=status.HTTP_200_OK)
            temp = nextDestinationForElevator(elevator).floorNumber
            if temp > elevator.currentFloor.floorNumber or elevator.currentFloor == None:
                return Response({"message":f"Elevator {label} going up"},status=status.HTTP_200_OK)
            else:
                return Response({"message":f"Elevator {label} going down"},status=status.HTTP_200_OK)
        except:
            return Response({"message":f"Elevator with label={label} does not exist"},status=status.HTTP_400_BAD_REQUEST)