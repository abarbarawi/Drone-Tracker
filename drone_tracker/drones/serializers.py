from rest_framework import serializers
from .models import Drone
from django.contrib.auth.models import User


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
class OnlineDroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['serial', 'latitude', 'longitude', 'last_seen'] 
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Get the password from validated data
        password = validated_data.pop('password')
        
        # Create the user without saving the password directly
        user = User(**validated_data)
        
        # Use set_password to hash the password
        user.set_password(password)
        
        # Save the user to the database
        user.save()
        return user
