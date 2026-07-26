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
        self.v2_url = f"https://{self.bridge_ip}/clip/v2"
        self._cache = None
        self._cache_time = 0
        self._v2_cache = None
        self._v2_cache_time = 0
        self._scenes_cache = None
        self._scenes_cache_time = 0
        
        
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
    
    
    def _get_v2(self, endpoint: str):
        url = f"{self.v2_url}/{endpoint}"
        self._log("GET V2", endpoint)
        response = requests.get(
            url, 
            headers={
                "hue-application-key": self.username
            },
            verify=False,
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        self._log("V2 RESPONSE", data)
        return data
    
    
    def _put(self, endpoint: str, payload: dict):
         url = f"{self.base_url}/{endpoint}"
         self._log("PUT", endpoint, payload)
         response = requests.put(url, json=payload, timeout=5)
         response.raise_for_status()
         data = response.json()
         self._log("RESPONSE", data)
         return data
    
     
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
        now = time.time()
        if (
            self._scenes_cache is not None
            and (now - self._scenes_cache_time) < 60
        ):
            self._log("Using scenes cache")
            return self._scenes_cache
        
        data = self._get("scenes")
        
        self._scenes_cache = data
        self._scenes_cache_time = now
        
        return data 
    
    def get_v2_scenes(self):
        now = time.time()
        if (
            self._v2_cache is not None
            and (now - self._v2_cache_time) < 60
        ):
            self._log("Using V2 cache")
            return self._v2_cache
        data = self._get_v2("resource/scene")
        self._v2_cache = data
        self._v2_cache_time = now
        return data
    
    
    def get_scene(self, scene_id: str):
        scenes = self.get_scenes()
        
        scene = scenes.get(scene_id)
        
        if scene is None:
            self._log("Scene not found:", scene_id)
            
        return scene
    
    
    def activate_scene(self, scene_id: str):
        scene = self.get_scene(scene_id)
        
        if scene is None:
            self._log("Cannot activate scene:", scene_id)
            return
        
        group = scene.get("group")
        if not group:
            self._log("Scene has no group:", scene_id)
            return
        
        payload ={"scene": scene_id}
        self._put(f"groups/{group}/action", payload)
        self._invalidate_cache()