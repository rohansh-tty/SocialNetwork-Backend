from app.models import User, FriendRequest
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'avatar']
        
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'avatar', 'name']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
