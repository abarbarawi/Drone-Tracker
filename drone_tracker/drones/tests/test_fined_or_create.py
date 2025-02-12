from django.test import TestCase
from unittest.mock import patch
from drones.models import Drone, FlightPath
from drones.repositories.drone_repository import DroneRepository
import random
import string

class DroneRepositoryTests(TestCase):
    def generate_serial(self):
        length = 21
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_string
    
    @patch('drones.repositories.drone_repository.DroneRepository.is_drone_dangerous')
    def test_fined_or_create_existing_drone(self, mock_is_dangerous):
        """Test updating an existing drone"""
        
        # Arrange
        serial = "1581F6Q8D81F6Q8DEYN10"
        old_latitude = 30.0
        old_longitude = 40.0
        new_latitude = 32.0
        new_longitude = 42.0
        
        # Mock dangerous status
        mock_is_dangerous.return_value = (False, "")

        # Create an existing drone
        Drone.objects.create(
            serial=serial,
            latitude=old_latitude,
            longitude=old_longitude,
            height=100.0,
            horizontal_speed=10.0,
            vertical_speed=5.0,
            is_dangerous=False,
            danger_reason=""
        )

        data = {
            "latitude": new_latitude,
            "longitude": new_longitude,
            "height": 150.0,
            "horizontal_speed": 12.0,
            "vertical_speed": 6.0
        }

        # Act
        drone_repo = DroneRepository()
        drone, created = drone_repo.fined_or_create(serial, data)
        
        # Assert
        self.assertFalse(created)  # It shouldn't create a new drone
        self.assertEqual(drone.latitude, new_latitude)
        self.assertEqual(drone.longitude, new_longitude)
        self.assertEqual(drone.height, 150.0)
        
        # Ensure a new FlightPath is created since the location changed
        self.assertEqual(FlightPath.objects.count(), 1)

    @patch('drones.repositories.drone_repository.DroneRepository.is_drone_dangerous')
    def test_fined_or_create_new_drone(self, mock_is_dangerous):
        """Test creating a new drone"""
        
        # Arrange
        serial = self.generate_serial()
        mock_is_dangerous.return_value = (False, "")
        
        data = {
            "latitude": 30.0,
            "longitude": 40.0,
            "height": 100.0,
            "horizontal_speed": 10.0,
            "vertical_speed": 5.0
        }

        # Act
        drone_repo = DroneRepository()
        drone, created = drone_repo.fined_or_create(serial, data)
        
        # Assert
        self.assertTrue(created)  # A new drone should be created
        self.assertEqual(drone.serial, serial)
        self.assertEqual(drone.latitude, 30.0)
        self.assertEqual(drone.longitude, 40.0)

    @patch('drones.repositories.drone_repository.DroneRepository.is_drone_dangerous')
    def test_fined_or_create_location_changed_creates_flightpath(self, mock_is_dangerous):
        """Test that a new FlightPath is created when location changes"""
        
        # Arrange
        serial = "1581F6Q8D81F6Q8DEYN10"
        old_latitude = 30.0
        old_longitude = 40.0
        new_latitude = 33.0
        new_longitude = 43.0
        
        # Mock dangerous status
        mock_is_dangerous.return_value = (False, "")
        
        # Create an existing drone
        Drone.objects.create(
            serial=serial,
            latitude=old_latitude,
            longitude=old_longitude,
            height=100.0,
            horizontal_speed=10.0,
            vertical_speed=5.0,
            is_dangerous=False,
            danger_reason=""
        )

        data = {
            "latitude": new_latitude,
            "longitude": new_longitude,
            "height": 150.0,
            "horizontal_speed": 12.0,
            "vertical_speed": 6.0
        }

        # Act
        drone_repo = DroneRepository()
        drone, created = drone_repo.fined_or_create(serial, data)
        
        # Assert
        self.assertFalse(created)  # No new drone created
        self.assertEqual(drone.latitude, new_latitude)
        self.assertEqual(drone.longitude, new_longitude)
        
        # Ensure a new FlightPath is created
        self.assertEqual(FlightPath.objects.count(), 1)

    def test_fined_or_create_invalid_data(self):
        """Test that invalid data raises an error (if applicable)"""
        
        # Test with missing required data or invalid values
        data = {
            "latitude": "not_a_float",  # Invalid latitude
            "longitude": 40.0,
            "height": 100.0,
            "horizontal_speed": 10.0,
            "vertical_speed": 5.0
        }
        
        drone_repo = DroneRepository()
        with self.assertRaises(ValueError):  # Adjust according to how errors are raised
            drone_repo.fined_or_create("DR126", data)
