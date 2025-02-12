from django.db import models
class Drone(models.Model):
    serial = models.CharField(max_length=21, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.FloatField()
    horizontal_speed = models.FloatField()
    vertical_speed = models.FloatField()
    is_dangerous = models.BooleanField(default=False)
    danger_reason = models.CharField(max_length=255, blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Drone {self.serial}"
    
class FlightPath(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name="flight_paths")
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.drone.serial} - {self.timestamp}"

