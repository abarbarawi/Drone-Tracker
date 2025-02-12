from rest_framework import serializers
from .models import Drone

class OnlineDroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['serial', 'latitude', 'longitude', 'last_seen']  # Only required fields
