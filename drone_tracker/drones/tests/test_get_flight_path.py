from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User

class GetDroneFlightPathTests(APITestCase):
    def setUp(self):
        self.valid_serial = "DRONE123"
        self.invalid_serial = "INVALID123"
        self.flight_path_url = f"/api/drones/flight-path/{self.valid_serial}/"
        self.invalid_flight_path_url = f"/api/drones/flight-path/{self.invalid_serial}/"
        self.geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[-122.4194, 37.7749], [-118.2437, 34.0522]]
                    },
                    "properties": {"drone_id": self.valid_serial}
                }
            ]
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post('/api/drones/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  
        
        self.token = response.data.get('access') 

    @patch("drones.repositories.drone_repository.DroneRepository.get_flight_path_as_geojson")
    def test_get_flight_path_success(self, mock_get_flight_path):
        """Test API returns flight path successfully"""
        mock_get_flight_path.return_value = self.geojson_data

        response = self.client.get(self.flight_path_url,HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.geojson_data)

    @patch("drones.repositories.drone_repository.DroneRepository.get_flight_path_as_geojson")
    def test_get_flight_path_not_found(self, mock_get_flight_path):
        """Test API returns 404 when drone not found"""
        mock_get_flight_path.return_value = None

        response = self.client.get(self.invalid_flight_path_url,HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "Drone not found or no flight data"})

  
    @patch("drones.repositories.drone_repository.DroneRepository.get_flight_path_as_geojson")
    def test_get_flight_path_internal_server_error(self, mock_get_flight_path):
        """Test API returns 500 when an internal server error occurs"""
        mock_get_flight_path.side_effect = Exception("Unexpected error")

        response = self.client.get(self.flight_path_url,HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"error": "Internal server error"})
              