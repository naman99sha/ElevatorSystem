from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializer import adminUserSerializer

# Create your views here.
class CreateAdmin(generics.GenericAPIView):
    serializer_class = adminUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": adminUserSerializer(user,context=self.get_serializer_context).data
        })
    