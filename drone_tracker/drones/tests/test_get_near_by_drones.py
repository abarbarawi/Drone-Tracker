from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class GetNearbyDronesTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
    
        self.user = User.objects.create_user(username='testuser', password='testpassword')

       
        response = self.client.post('/api/drones/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  
        
        self.token = response.data.get('access') 
    @patch('drones.repositories.drone_repository.DroneRepository.get_drones_within_radius')
    def test_get_nearby_drones_success(self, mock_get_drones_within_radius):
        """Test fetching drones within a radius successfully"""
        # Mock the repository call
        mock_get_drones_within_radius.return_value = [
            {"serial": "DRONE123", "latitude": 40.7128, "longitude": -74.0060},
            {"serial": "DRONE456", "latitude": 40.7130, "longitude": -74.0070},
        ]
        
        # Create a valid request payload
        data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "distance": 1000
        }
        
        response = self.client.post("/api/drones/nearby/", data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Assert correct response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We mocked 2 drones
        self.assertEqual(response.data[0]["serial"], "DRONE123")

    def test_get_nearby_drones_missing_parameters(self):
        """Test API returns 400 when missing required parameters"""
        data = {}  # Missing all required fields
        response = self.client.post("/api/drones/nearby/", data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Missing required parameters: latitude, longitude, distance"})

    def test_get_nearby_drones_invalid_parameters(self):
        """Test API returns 400 when parameters are invalid"""
        data = {
            "latitude": "invalid",  # Invalid latitude
            "longitude": "invalid",  # Invalid longitude
            "distance": "invalid"  # Invalid distance
        }
        response = self.client.post("/api/drones/nearby/", data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "latitude, longitude, and distance must be numbers"})

    def test_get_nearby_drones_invalid_json(self):
        """Test API returns 400 for invalid JSON format"""
        invalid_json_data = '{"latitude": 40.7128, "longitude": -74.0060, "distance": 1000'  # Missing closing brace
        response = self.client.post("/api/drones/nearby/", invalid_json_data, content_type='application/json',HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Invalid JSON format"})
