from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username','email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        def create(self, validated_data):
            email = validated_data.get('email', None)
            if email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError('This email address is already exists.')
            return User.objects.create_user(**validated_data)


