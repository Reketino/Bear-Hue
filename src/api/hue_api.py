import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HueAPI:
    
    
    def __init__(self, bridge_ip: str):
        self.bridge_ip = bridge_ip
        self.username = os.getenv("HUE_USERNAME")
        if not self.username:
            raise ValueError("Your HUE_USERNAME is not found in .env")
        self.base_url = f"http://{self.bridge_ip}/api/{self.username}"
        
        
    def get_lights(self):
        """Json returning raw lights connected to Hue Bridge"""
        url = f"{self.base_url}/lights"
        response = requests.get(url)
        return response.json()
    
    
    def list_lights(self):
        """Json returning light id w/ name"""
        lights = self.get_lights()
        return {
            light_id: light["name"]
            for light_id, light in lights.items()
        }
        
    
    def set_light(self, light_id: int, on: bool):
        """Function for turning lights on or off"""   
        url = f"{self.base_url}/lights/{light_id}/state"
        payload = {"on": on} 
        requests.put(url, json=payload)
        
        
    def get_all_lights_state(self):
        """Limit for API"""
        url = f"{self.base_url}/lights"
        response = requests.get(url)
        return response.json()
        
        
    def get_light_state(self, light_id: int) -> bool:
        """Returning True if light is on, False if not"""
        url = f"{self.base_url}/lights/{light_id}"
        response = requests.get(url).json()
        return response["state"]["on"]
    
    
    def get_brightness(self, light_id: int) -> int:
        """Collecting brightness from hue bridge"""
        url = f"{self.base_url}/lights/{light_id}"
        response = requests.get(url).json()
        return response["state"]["bri"]
    
    
    def set_brightness(self, light_id: int, bri: int):
        """Ajusting Brightness for all lights"""
        url = f"{self.base_url}/lights/{light_id}/state"
        payload = {"bri": bri}
        requests.put(url, json=payload)