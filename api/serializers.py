from django.contrib.messages.storage.cookie import MessageSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserImage

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

class ResponseMessageSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()

class AuthResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = ResponseMessageSerializer()

class UserImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ('id', 'url', 'description')

    def get_url(self, obj):
        return obj.image.url