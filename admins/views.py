from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializer import adminUserSerializer

# TO CREATE AN ELEVATOR ADMIN
# BODY = {"email":<email>, "password":<password>}
# PASSWORD MUST HAVE AT LEAST 8 CHARACTERS, WITH AT LEAST 1 UPPER CASE, 1 LOWER CASE, 1 NUMERIC AND EITHER '@','$' OR '_' IN IT
class CreateAdmin(generics.GenericAPIView):
    serializer_class = adminUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": adminUserSerializer(user,context=self.get_serializer_context).data
        })
    