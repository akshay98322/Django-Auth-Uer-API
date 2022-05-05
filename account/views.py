from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import (UserRegistrationSerializer,
                          UserLoginSerializer, 
                          UserProfileSerializer, 
                          UserChangePassSerializer,
                          SendPassResetMailSerializer,
                          UserPassResetSerializer)
from .renderers import UserRenderer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationApiView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Success..!'}, status=status.HTTP_201_CREATED)


class UserLoginApiView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success..!'}, status=status.HTTP_200_OK)
        return Response({'errors': {'non_field_errors': ["Email or Password is incorrect."]}}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserProfileApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePassSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid()
        return Response({'msg': 'Password changed successfully..!'}, status=status.HTTP_200_OK)


class SendPassResetMailApiView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPassResetMailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset mail sent successfully..!'}, status=status.HTTP_200_OK)


class UserPassResetApiView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, token, uid, format=None):
        serializer = UserPassResetSerializer(data=request.data, context = {'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password changed successfully..!'}, status=status.HTTP_200_OK)