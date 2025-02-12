from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from drones.models import Drone
from django.contrib.auth.models import User

class DroneViewsTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.client = APIClient()

        # Create a test drone
        self.drone = Drone.objects.create(
            serial="Dr000",
            latitude=10.0,
            longitude=20.0,
            height=50.0,
            horizontal_speed=5.0,
            vertical_speed=2.0,
            is_dangerous=False,
            danger_reason=""
        )
      
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post('/api/drones/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  
        
        self.token = response.data.get('access') 

    def test_get_drone_by_valid_serial(self):
        """Test fetching a drone with a valid serial number"""
        response = self.client.get(f'/api/drones/serial/{self.drone.serial}/',HTTP_AUTHORIZATION=f'Bearer {self.token}')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], self.drone.serial)

    def test_get_drone_by_invalid_serial(self):
        """Test fetching a drone with an invalid serial number"""
        response = self.client.get('/api/drones/serial/INVALID_SERIAL/',HTTP_AUTHORIZATION=f'Bearer {self.token}')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Drone not found")

    def test_get_drone_missing_serial(self):
        """Test fetching a drone with a missing serial parameter"""
        response = self.client.get('/api/drones/serial/',HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Missing serial
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should return 404 since the route doesn't match
