🚀 Drone Tracker System
A Django-based Drone Tracker System that allows users to monitor drones, track their flight paths, and retrieve real-time status updates. The system also provides JWT-based authentication for secure access.

📌 Features
Retrieve Drones: Get all registered drones .
Filter by Status: View online and dangerous drones separately.
Search by Serial or ID: Fetch specific drone details using their unique serial number or ID.
Flight Path Tracking: View the flight path of any drone.
Nearby Drones: Find drones near a given location using geolocation.
User Authentication: Register, login, and obtain JWT tokens for secure API access.

🛠️ Tech Stack
Backend: Django 5.1.6, Django REST Framework (DRF)
Database: SqlLite
Authentication: JWT (JSON Web Token)
Messaging: MQTT (paho-mqtt)
Geolocation: Haversine formula for distance calculations
Testing: Pytest, pytest-django

📥 Installation
Prerequisites
Python 3.11.0
mosquitto use this link to download it (https://mosquitto.org/download/)
Virtual environment (recommended)
python -m venv venv  
source venv/bin/activate  # Windows: venv\Scripts\activate  
pip install -r requirements.txt  


> Django commands:
python manage.py makemigrations drones
python manage.py migrate
python manage.py runserver 8080

🔗 API Endpoints 
api documentation (https://documenter.getpostman.com/view/17808531/2sAYXCidPD)
🚁 Drone Management
Method	Endpoint	Description
GET	/	Get all drones
GET	/dangerous/	Get all dangerous drones
GET	/online/	Get all online drones
GET	/serial/<str:serial>/	Get a drone by serial number
GET	/<int:drone_id>/	Get a drone by ID
GET	/flight-path/<str:serial>/	Get a drone’s flight path
POST	/nearby/	Find drones near a location
🔐 Authentication
Method	Endpoint	Description
POST	/api/token/	Obtain JWT Token
POST	/api/token/refresh/	Refresh JWT Token
POST	/register/	Register a new user
POST	/login/	Login and get a token

Run Tests : 
>pytest .\drones\tests\

env values
ENV=local
MQTT_BROKER = "localhost"

>mosquitto :
how to send message to mqtt using cmd
>cd C:\Program Files\mosquitto>
if you face a preoblem run cmd as administrator
>mosquitto_pub -h localhost -t "thing/product/{serial}/osd" -m {msg}
MQTT_PORT = 1883
MQTT_TOPIC = "thing/product/+/osd"


