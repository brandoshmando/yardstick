from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from yardstick.serializers import SignInSerializer, SignInResponseSerializer, OraganizationPostSerializer
from yardstick.models import Organization

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


class OrganizationCreate(generics.CreateAPIView):
    serializer_class = OraganizationPostSerializer
    permission_class = (permissions.AllowAny)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            org, mgr, usr = Organization.objects.create_account(
                    name=serializer.data.get('name'),
                    first_name=serializer.data.get('first_name'),
                    last_name=serializer.data.get('last_name'),
                    unique_identifier=serializer.data.get('unique_identifier'),
                    email=serializer.data.get('email'),
                    password=serializer.data.get('password')
                  )
            signin_serializer = SignInResponseSerializer(instance=usr)
            return Response(signin_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
