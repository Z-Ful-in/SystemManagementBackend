from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import RegisterSerializer, AuthResponseSerializer


# Create your views here.


@api_view(['POST'])
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
        }))
    else:
        return  JsonResponse(
            AuthResponseSerializer({
            'success': False,
            'message':{
                'message': serialize.errors,
                'code': 400
            }
        }))


@api_view(['POST'])
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
            })
        )
    else:
        return JsonResponse(
            AuthResponseSerializer({
                'success': False,
                'message':{
                    'message': 'username or password is incorrect',
                    'code': 401
                }
            })
        )


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse(
        AuthResponseSerializer({
            'success': True,
            'message':{
                'message': 'logout successfully',
                'code': 202
            }
        })
    )