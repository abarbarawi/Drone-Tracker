import paho.mqtt.client as mqtt
import json
import threading
from dotenv import load_dotenv
import os
import re
from drones.repositories.drone_interface import BaseRepository
from drones.repositories.drone_repository import DroneRepository
load_dotenv()


class MQTTClient:
    def __init__(self,repository: BaseRepository = DroneRepository()):
                
        # MQTT Broker Settings
        self.MQTT_BROKER = os.getenv("MQTT_BROKER")
        self.MQTT_PORT = int(os.getenv("MQTT_PORT"))
        self.MQTT_TOPIC = os.getenv("MQTT_TOPIC")
        self.repository = repository

    def on_connect(self,client, userdata, flags, rc):
        """ Callback when client connects to the MQTT broker. """
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(self.MQTT_TOPIC)
            print(f"Subscribed to topic: {self.MQTT_TOPIC}")
        else:
            print(f"Connection failed with error code {rc}")

    def on_message(self, client,userdata,msg):
        try:
            print(f"msg: {msg.topic}")
            data = json.loads(msg.payload.decode("utf-8"))
            serial = self.get_serial(msg.topic) # Ensure each drone has a unique serial number
            drone,created=self.repository.fined_or_create(serial,data)
            print(f"{'Created' if created else 'Updated'} drone {drone.serial}")
        except Exception as e : 
            print(f"error processing mqtt msg :{e}")
    def start_mqtt(self):
        """ Start the MQTT client in a background thread. """
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)

        # Run MQTT in a separate thread to avoid blocking Django
        mqtt_thread = threading.Thread(target=client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()
        print("MQTT Client Started!")
    def get_serial(self,topic):
        topic = topic  
        serial=None
        match = re.search(r"product/([A-Za-z0-9]+)/", topic)
        if match:
            serial = match.group(1)
        return serial

