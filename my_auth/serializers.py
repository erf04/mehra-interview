from rest_framework import serializers
from .models import User
from typing import Dict
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # for save call 
    def create(self, validated_data:Dict) -> User: 
        user = User.objects.create_user(**validated_data)
        return user
    
    # validate if the username unique or not 
    def validate_username(self, username:str) -> str:

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")

        return username
    

    # validate password more then 8 letters 
    def validate_password(self, password:str) -> str:
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return password
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']