from django.apps import AppConfig

class DronesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drones"
    def ready(self):
        from .mqtt_client import MQTTClient
        client=MQTTClient()
        client.start_mqtt()