from rest_framework import serializers
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
    new_password = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(max_length=255, style= {'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['new_password', 'new_password2']
    
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        user = self.context.get('user')
        if new_password != new_password2:
            raise serializers.ValidationError("Passwords must match.")
        user.set_password(new_password)
        user.save()
        return attrs


        