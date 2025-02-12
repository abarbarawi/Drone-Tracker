from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from drones.models import Drone
from django.contrib.auth.models import User

class DroneViewsTests(TestCase):
  
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        Drone.objects.create(serial="DR001", latitude=30.0, longitude=40.0,height=30,horizontal_speed=20,vertical_speed=0)
        Drone.objects.create(serial="DR002", latitude=35.0, longitude=45.0,height=10,horizontal_speed=0,vertical_speed=0)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

       
        response = self.client.post('/api/drones/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  
        
        self.token = response.data.get('access') 

    def test_get_drones(self):
        """Test the GET  API"""
        response = self.client.get('/api/drones/',HTTP_AUTHORIZATION=f'Bearer {self.token}')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        self.assertEqual(response.data[0]['serial'], "DR001")
