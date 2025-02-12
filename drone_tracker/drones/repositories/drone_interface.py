from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Abstract base repository to enforce method implementation"""
    
    @abstractmethod
    def fined_or_create(self,serial:str,data:object):
        pass
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, identifier:int):
        pass
    @abstractmethod
    def get_all_dangerous(self):
        pass
    @abstractmethod
    def get_online_drones(self):
        pass
    @abstractmethod
    def  get_by_serial(self, serial:str):
        pass
    @abstractmethod
    def  get_flight_path_as_geojson(self, serial:str):
        pass
    @abstractmethod
    def get_drones_within_radius(self,lat:float,lon:float,radius_km:float):
        pass