from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        if password != password2:
            raise serializers.ValidationError("Passwords must match.")
        return data
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name']


class UserChangePassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords must match.")
        user.set_password(password)
        user.save()
        return attrs

class SendPassResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f'http://127.0.0.1:3000/api/user/reset-pass/{uid}/{token}'
            print(reset_link)
            return attrs
        else:
            raise serializers.ValidationError("Email is not registered.")


class UserPassResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Passwords must match.")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Invalid token.")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Invalid token.")
        

        