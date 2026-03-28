import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HueAPI:
    
    def __init__(self, bridge_ip: str, debug: bool = False):
        self.bridge_ip = bridge_ip
        self.debug = debug
        self.username = os.getenv("HUE_USERNAME")
        if not self.username:
            raise ValueError("Your HUE_USERNAME is not found in .env")
        self.base_url = f"http://{self.bridge_ip}/api/{self.username}"
        self._cache = None
        self._cache_time = 0
        
   # ------ Internal Helpers, when Superman needs help -------
   
    def _log(self, *args):
        if self.debug:
            print("[HUEAPI]", *args)
   
        
    def _get(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"
        self._log("GET", endpoint)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
    
    def _put(self, endpoint: str, payload: dict):
         url = f"{self.base_url}/{endpoint}"
         response = requests.put(url, json=payload, timeout=5)
         response.raise_for_status()
         return response.json()
    
     
    def _invalidate_cache(self):
        self._cache = None
        self._cache_time = 0
    
        
    # ------- Public API'S ----------
    
        
    def get_all_lights_state(self):
        now = time.time()
        if self._cache is not None and (now - self._cache_time) < 0.5:
            return self._cache
        data = self._get("lights")
        self._cache = data
        self._cache_time = now
        return data
        
        
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
        self._invalidate_cache()
        
    
    def set_brightness(self, light_id: int, bri: int):
        payload = {
            "bri": bri,
            "transitiontime": 5
        }
        self._put(f"lights/{light_id}/state",payload)
        self._invalidate_cache()
    
        
    def set_group_brightness(self, bri: int):
        lights = self.get_all_lights_state()
        payload = {
            "bri": bri,
            "transitiontime": 5
        }
        for light_id in lights:
            self._put(f"lights/{light_id}/state", payload)
        self._invalidate_cache()
            
            
    # ------- Philip's Hue Scenes ----------
    
    def get_scenes(self):
        return self._get("scenes")
    
    
    def get_scene(self, scene_id: str):
        return self._get(f"scenes/{scene_id}")
    
    
    def activate_scene(self, scene_id: str):
        scene = self.get_scene(scene_id)
        if isinstance(scene, list):
            scene = scene[0]
        group = scene.get("group")
        if not group:
            return
        payload ={"scene": scene_id}
        self._put(f"groups/{group}/action", payload)
        self._invalidate_cache()