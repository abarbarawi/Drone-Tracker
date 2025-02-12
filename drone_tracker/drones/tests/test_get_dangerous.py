from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from drones.models import Drone
from django.contrib.auth.models import User

class DroneViewsTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()       
        self.user = User.objects.create_user(username='testuser', password='testpassword')

       
        response = self.client.post('/api/drones/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  
        
        self.token = response.data.get('access') 
    
    def test_get_drones(self):
        """Test the GET  API"""
        response = self.client.get('/api/drones/dangerous/',HTTP_AUTHORIZATION=f'Bearer {self.token}')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(drone["is_dangerous"] for drone in response.data), "Some returned drones are not dangerous")
