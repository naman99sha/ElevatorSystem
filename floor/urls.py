from django.urls import path
from .views import createFloors

urlpatterns = [
    path("create",createFloors,name="create-floors"),
]