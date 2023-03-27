from django.urls import path
from .views import CreateElevator, RequestListElevator, ElevatorGoUp, ElevatorGoDown, ChangeElevatorMoving, ChangeElevatorStatus, GetElevatorCurrentFloor, OpenElevatorDoor, CloseElevatorDoor, ElevatorGoingUpOrDown, GetElevatorNextDestination

urlpatterns = [
    path("create",CreateElevator.as_view(),name="create-elevator"),
    path("<label>/request-list",RequestListElevator.as_view(),name="elevator-request-list"),
    path("<label>/up",ElevatorGoUp.as_view(),name="elevator-go-up"),
    path("<label>/down",ElevatorGoDown.as_view(),name="elevator-go-down"),
    path("<label>/change-moving",ChangeElevatorMoving.as_view(),name="change-elevator-moving"),
    path("<label>/set-status",ChangeElevatorStatus.as_view(),name="set-status"),
    path("<label>/current-floor",GetElevatorCurrentFloor.as_view(),name="get-current-floor"),
    path("<label>/open-door",OpenElevatorDoor.as_view(),name="open-elevator-door"),
    path("<label>/close-door",CloseElevatorDoor.as_view(),name="close-elevator-door"),
    path("<label>/next-destination",GetElevatorNextDestination.as_view(),name="elevator-next-destination"),
    path("<label>/movement",ElevatorGoingUpOrDown.as_view(),name="elevator-movement")
]