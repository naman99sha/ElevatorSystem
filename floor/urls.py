from django.urls import path
from .views import createFloors, requestElevator

urlpatterns = [
    path("create",createFloors,name="create-floors"),
    path("<floorNumber>/request-elevator",requestElevator,name="request-elevator")
]