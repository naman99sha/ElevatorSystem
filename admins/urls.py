from .views import CreateAdmin
from django.urls import path

urlpatterns = [
    path('create',CreateAdmin.as_view(),name='create-admin'),
]