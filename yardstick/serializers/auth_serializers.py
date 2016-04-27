from rest_framework import serializers
from rest_framework.authtoken.models import Token

from yardstick.models import AuthUser

class SignUpResponseSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key
