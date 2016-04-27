from rest_framework import serializers

class OraganizationPostSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    first_name = serializers.CharField(max_length=64, required=False)
    last_name = serializers.CharField(max_length=64, required=False)
    email = serializers.EmailField(max_length=256, required=False)
    unique_identifier = serializers.CharField(max_length=256, required=False)
    password = serializers.CharField(max_length=512, style={'input_type':'password'})
