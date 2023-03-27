from django.urls import path
from .views import CreateElevator, RequestListElevator

urlpatterns = [
    path("create",CreateElevator.as_view(),name="create-elevator"),
    path("<label>/request-list",RequestListElevator.as_view(),name="elevator-request-list"),
]