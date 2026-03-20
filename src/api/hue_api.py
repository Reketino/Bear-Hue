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
        
        
    def _get(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
    
    def _put(self, endpoint: str, payload: dict):
         url = f"{self.base_url}/{endpoint}"
         response = requests.put(url, json=payload, timeout=5)
         response.raise_for_status()
         return response.json()
        
        
    def get_all_lights_state(self):  
        return self._get("lights")
        
        
    def list_lights(self):
        lights = self.get_all_lights_state()
        return {
            int(light_id): data["name"]
            for light_id, data in lights.items()
        }
        
        
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
        payload = {
            "bri": bri,
            "transitiontime": 5
            }
        requests.put(url, json=payload)