from django.contrib import admin
from .models import Drone,FlightPath

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('serial', 'latitude', 'longitude', 'height', 'last_seen', 'is_dangerous')
    search_fields = ('serial',)

@admin.register(FlightPath)
class FlightPathAdmin(admin.ModelAdmin):
    # Access the drone's serial through the related drone
    def get_drone_serial(self, obj):
        return obj.drone.serial  # Accessing the serial through the drone ForeignKey
    
    get_drone_serial.short_description = 'Drone Serial'  # This is the label that will appear in the admin

    list_display = ('get_drone_serial', 'latitude', 'longitude', 'timestamp')  # Use the custom method in list_display
    search_fields = ('drone__serial',)  # Allow search by drone serial
