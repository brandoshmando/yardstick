from rest_framework import serializers
from rest_framework.authtoken.models import Token

from yardstick.models import AuthUser

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'}
    )


class SignInResponseSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key


class OraganizationPostSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    first_name = serializers.CharField(max_length=64, required=False)
    last_name = serializers.CharField(max_length=64, required=False)
    email = serializers.EmailField(max_length=256, required=True)
    unique_identifier = serializers.CharField(max_length=256, required=False)
    password = serializers.CharField(max_length=512, style={'input_type':'password'})
