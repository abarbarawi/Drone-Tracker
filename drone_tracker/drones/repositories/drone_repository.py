from drones.repositories.drone_interface import BaseRepository
from drones.models import Drone,FlightPath
from datetime import timedelta
from django.utils import timezone
from math import radians, cos
from haversine import haversine, Unit
from typing import Optional

class DroneRepository(BaseRepository):
    """Repository for Drone model"""
    def fined_or_create(self,serial:float,data:object):
        old_drone = Drone.objects.filter(serial=serial).first()       
        is_drone_dangerous,reason=self.is_drone_dangerous(data)
        latitude = float(data.get("latitude", 0.0))
        longitude = float(data.get("longitude", 0.0))
        height = float(data.get("height", 0.0))
        horizontal_speed = float(data.get("horizontal_speed", 0.0))
        vertical_speed = float(data.get("vertical_speed", 0.0))
        drone, created = Drone.objects.update_or_create(
            serial=serial,
            defaults={
                "latitude": latitude,
                "longitude": longitude,
                "height": height,
                "horizontal_speed": horizontal_speed,
                "vertical_speed": vertical_speed,
                "is_dangerous":is_drone_dangerous,
                "danger_reason":reason
            }
        )
        if old_drone is not None:
            if old_drone.latitude != latitude or old_drone.longitude != longitude:
                FlightPath.objects.create(drone=drone, latitude=latitude, longitude=longitude)
        else:
                FlightPath.objects.create(drone=drone, latitude=latitude, longitude=longitude)
        

        return drone,created
    def get_all(self)->list[Drone]:
        return Drone.objects.all()

    def get_by_id(self, identifier:int)->Optional[Drone]:
        print(identifier)

        return Drone.objects.filter(id=identifier).first()

        
    def is_drone_dangerous(self,data:object)->tuple[bool, str]:
        is_dangerous = False
        reason = []
        max_height = 500  # meters
        max_speed = 10  # m/s

        if data['height'] > max_height:
            is_dangerous = True
            reason.append(f"Drone height is higher than max allowed height ({max_height}m).")
        
        if data['horizontal_speed'] > max_speed:
            is_dangerous = True
            reason.append(f"Drone speed is higher than max allowed speed ({max_speed} m/s).")

        danger_reason = " ".join(reason) if reason else "None"


        return is_dangerous, danger_reason
    def get_all_dangerous(self)-> list[Drone]:
        return Drone.objects.filter(is_dangerous=True)
    def get_online_drones(self)->list[Drone]:
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        return Drone.objects.filter(last_seen__gte=one_minute_ago)
    def get_by_serial(self, serial:str)->Optional [Drone]:
        return Drone.objects.filter(serial__icontains=serial).first()
     
    
    def get_flight_path_as_geojson(self,serial:str)->Optional [dict]:
        
        drone = Drone.objects.get(serial=serial)
        path_points = FlightPath.objects.filter(drone=drone).order_by("timestamp")

        if not path_points.exists():
            return None

        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        coordinates = []

        for point in path_points:
            coordinates.append([point.longitude, point.latitude]) 

        geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {}
        })

        return geojson

        

    def calculate_bounding_box(self,latitude:float, longitude:float, radius_km:float=5.0)->tuple[float, float,float,float]:
        """
        Calculate the latitude and longitude range (bounding box) 
        within a given radius (in km) around a central point.

        :param latitude: Central latitude (float)
        :param longitude: Central longitude (float)
        :param radius_km: Radius in kilometers (default is 5 km)
        :return: (min_lat, max_lat, min_lon, max_lon) as a tuple
        """

        # Convert latitude to radians for the cosine function
        lat_rad = radians(latitude)

        # Approximate degrees per km (Earth's radius ≈ 6371 km)
        lat_degree_km = 1 / 111  # 1 degree ≈ 111 km
        lon_degree_km = 1 / (111 * cos(lat_rad))  # Adjust for longitude

        # Compute latitude and longitude range
        lat_delta = radius_km * lat_degree_km
        lon_delta = radius_km * lon_degree_km

        min_lat = latitude - lat_delta
        max_lat = latitude + lat_delta
        min_lon = longitude - lon_delta
        max_lon = longitude + lon_delta

        return min_lat, max_lat, min_lon, max_lon
        

    def get_drones_within_radius(self,lat:float,lon:float,radius_km:float)->Optional [Drone]:
        # Get bounding box
        min_lat, max_lat, min_lon, max_lon = self.calculate_bounding_box(lat, lon, radius_km)
        print( min_lat, max_lat, min_lon, max_lon )
        # Filter drones within bounding box
        candidate_drones = Drone.objects.filter(
            latitude__range=(min_lat, max_lat),
            longitude__range=(min_lon, max_lon)
        )

        # Apply precise Haversine distance check
        reference_point = (lat, lon)
        nearby_drones = [
            {
                "serial": drone.serial,
                "latitude": drone.latitude,
                "longitude": drone.longitude,
                "distance_km": round(haversine(reference_point, (drone.latitude, drone.longitude), unit=Unit.KILOMETERS), 2),
            }
            for drone in candidate_drones
            if haversine(reference_point, (drone.latitude, drone.longitude), unit=Unit.KILOMETERS) <= radius_km
        ]

        return nearby_drones