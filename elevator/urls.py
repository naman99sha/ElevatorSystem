from django.urls import path
from .views import CreateElevator

urlpatterns = [
    path("create",CreateElevator.as_view(),name="create-elevator")
]