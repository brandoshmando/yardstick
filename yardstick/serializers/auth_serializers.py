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
