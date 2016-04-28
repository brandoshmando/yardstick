from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from yardstick.serializers import SignInSerializer, SignInResponseSerializer

class UserAuthentication(generics.CreateAPIView):
    serializer_class = SignInSerializer
    permission_class = (permissions.AllowAny)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                        email=serializer.data['email'],
                        password=serializer.data['password']
                   )
            if user:
                token = Token.objects.get(user=user)
                serializer_response = SignInResponseSerializer(instance=user)

                return Response(serializer_response.data, status.HTTP_200_OK)

            data = {
                'non_field_errors':["Invalid email and/or password combination. Please try again!"]
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
