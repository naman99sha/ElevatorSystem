from django.urls import path
from .views import CreateElevator, RequestListElevator, ElevatorGoUp, ElevatorGoDown, ChangeElevatorMoving, ChangeElevatorStatus

urlpatterns = [
    path("create",CreateElevator.as_view(),name="create-elevator"),
    path("<label>/request-list",RequestListElevator.as_view(),name="elevator-request-list"),
    path("<label>/up",ElevatorGoUp.as_view(),name="elevator-go-up"),
    path("<label>/down",ElevatorGoDown.as_view(),name="elevator-go-down"),
    path("<label>/change-moving",ChangeElevatorMoving.as_view(),name="change-elevator-moving"),
    path("<label>/set-status",ChangeElevatorStatus.as_view(),name="set-status"),
]