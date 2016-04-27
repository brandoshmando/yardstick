from rest_framework import generics, permissions, status
from rest_framework.response import Response

from yardstick.serializers import OraganizationPostSerializer, SignUpResponseSerializer
from yardstick.models import Organization

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
            signin_serializer = SignUpResponseSerializer(instance=usr)
            return Response(signin_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
