from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drones.repositories.drone_repository import DroneRepository
from drones.serializers import DroneSerializer,UserSerializer,OnlineDroneSerializer
import json
import logging
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

repository = DroneRepository()
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(request):
    """Fetch all drones"""
    try:
        drones = repository.get_all()
        serializer = DroneSerializer(drones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching drones: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_online_drones(request):
    """Fetch all online drones"""
    try:
        drones = repository.get_online_drones()
        serializer = OnlineDroneSerializer(drones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching online drones: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_id(request, drone_id):
    """Fetch a drone by ID"""
    try:
        # if drone_id:
        #     return Response({"error": "Invalid drone ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        drone = repository.get_by_id(drone_id)
        if not drone:
            return Response({"error": "Drone not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DroneSerializer(drone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching drone by ID {drone_id}: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_dangerous_drones(request):
    """Fetch all dangerous drones"""
    try:
        dangerous_drones = repository.get_all_dangerous()
        serializer = DroneSerializer(dangerous_drones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching dangerous drones: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_drone_by_serial(request, serial):
    """Fetch a drone by serial number"""
    try:
        if not serial:
            return Response({"error": "Serial number is required"}, status=status.HTTP_400_BAD_REQUEST)

        drone = repository.get_by_serial(serial)
        if not drone:
            return Response({"error": "Drone not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DroneSerializer(drone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching drone by serial {serial}: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_drone_flight_path(request, serial):
    """Fetch a drone's flight path as GeoJSON"""
    try:
     
        geojson = repository.get_flight_path_as_geojson(serial)
        if geojson is None:
            return Response({"error": "Drone not found or no flight data"}, status=status.HTTP_404_NOT_FOUND)

        return Response(geojson)
    except Exception as e:
        logger.error(f"Error fetching flight path for drone {serial}: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_nearby_drones(request):
    """Fetch drones within a given distance from a point"""
    try:
        data = json.loads(request.body)
        lat = data.get('latitude')
        lon = data.get('longitude')
        distance = data.get('distance')

        if lat is None or lon is None or distance is None:
            return Response({"error": "Missing required parameters: latitude, longitude, distance"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lon = float(lon)
            distance = float(distance)
        except ValueError:
            return Response({"error": "latitude, longitude, and distance must be numbers"}, status=status.HTTP_400_BAD_REQUEST)

        drones = repository.get_drones_within_radius(lat, lon, distance)
        return Response(drones, status=status.HTTP_200_OK)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error fetching nearby drones: {str(e)}",exc_info=True)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_user(request):
    """Create a new user"""
    try:
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "message": "User created successfully",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    """Login user and return JWT token"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            # Create JWT tokens (access and refresh)
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e :
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
