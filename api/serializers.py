from django.contrib.messages.storage.cookie import MessageSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserImage

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

class ResponseMessageSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url