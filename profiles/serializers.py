from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer



class UserSerializer(BaseUserSerializer):
    is_staff=serializers.BooleanField(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'phone_no', 'first_name', 'last_name', 'is_staff']




