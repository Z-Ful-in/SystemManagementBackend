import os
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import UserImage
from api.serializers import RegisterSerializer, AuthResponseSerializer, UserImageSerializer


# Create your views here.

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_view(request):
    serialize = RegisterSerializer(data=request.data)
    if serialize.is_valid():
        User.objects.create_user(**serialize.validated_data)
        return JsonResponse(
            AuthResponseSerializer({
            'success': True,
            'message':{
                'message': 'registered successfully',
                'code': 200
            }
        }).data)
    else:
        error_message = serialize.errors.get('username', ['Unknown error'])[0]
        return  JsonResponse(
            AuthResponseSerializer({
            'success': False,
            'message':{
                'message': error_message,
                'code': 400
            }
        }).data)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse(
            AuthResponseSerializer({
                'success': True,
                'message':{
                    'message': 'login successfully',
                    'code': 201
                }
            }).data
        )
    else:
        return JsonResponse(
            AuthResponseSerializer({
                'success': False,
                'message':{
                    'message': 'username or password is incorrect',
                    'code': 401
                }
            }).data
        )


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def logout_view(request):
    logout(request)
    return JsonResponse(
        AuthResponseSerializer({
            'success': True,
            'message':{
                'message': 'logout successfully',
                'code': 202
            }
        }).data
    )


@api_view(['GET'])
def get_user_images(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "success": False,
            "data": []
        })

    images = UserImage.objects.filter(user=user)
    serializer = UserImageSerializer(images, many=True, context={'request': request})
    return Response({
        "success": True,
        "data": serializer.data
    })


@api_view(['DELETE'])
def delete_image(request, id):
    try:
        userImage= UserImage.objects.get(id=id)
        if userImage.image.url.startswith(settings.MEDIA_URL):
            file_path = os.path.join(settings.MEDIA_ROOT, userImage.image.url.replace(settings.MEDIA_URL, ""))
            if os.path.isfile(file_path):
                os.remove(file_path)
        userImage.delete()
        return Response(True)
    except UserImage.DoesNotExist:
        return Response(False)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@parser_classes([MultiPartParser])
def upload_image(request):
    image = request.FILES.get('image')
    description = request.data.get('description')
    username = request.data.get('userName')

    if not (image and description and username):
        return Response(False)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(False)
    if not is_valid_image(image):
        return Response(False)
    UserImage.objects.create(user=user, description=description, image=image)
    return Response(True)

def is_valid_image(image: Optional[UploadedFile]) -> bool:
    if image is None:
        return False
    if image.size > 5 * 1024 * 1024:  # 大于5MB
        return False
    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
        return False
    from PIL import Image
    try:
        img = Image.open(image)
        if img.width < 300 or img.height < 300:
            return False
    except Exception:
        return False
    return True