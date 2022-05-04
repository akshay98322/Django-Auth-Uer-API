from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import UserRegistrationSerializer, UserLoginSerializer



class UserRegistrationApiView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Success..!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                return Response({'msg': 'Login Success..!'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': ["Email or Password is incorrect."]}}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)