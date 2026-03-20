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
        
   # ------ Internal Helpers, when Superman needs help -------
        
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
        
    # ------- Public API'S ----------
        
    def get_all_lights_state(self):  
        return self._get("lights")
        
        
    def list_lights(self):
        lights = self.get_all_lights_state()
        return {
            int(light_id): data["name"]
            for light_id, data in lights.items()
        }
        
        
    def set_light(self, light_id: int, on: bool):
        payload = {
            "on": on,
            "transitiontime": 2 if on else 6
        }
        self._put(f"lights/{light_id}/state", payload)
        
    
    def set_brightness(self, light_id: int, bri: int):
        payload = {
            "bri": bri,
            "transitiontime": 5
        }
        self._put(f"lights/{light_id}/state",payload)