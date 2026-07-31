import time
import os
from pathlib import Path
from dotenv import load_dotenv
from src.api.hue_https import HueHTTPS


load_dotenv()

CA_BUNDLE = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "certificates"
    / "huebridge_cacert_bundle.pem"
)

LIGHT_CACHE_SECONDS = 0.5
SCENE_CACHE_SECONDS = 60

LIGHT_ON_TRANSITION = 2
LIGHT_OFF_TRANSITION = 6
BRIGHTNESS_TRANSITION = 1

class HueAPI:
    
    def __init__(
        self, 
        bridge_ip: str, 
        debug: bool = False
    ):
        self.bridge_ip = bridge_ip
        self.debug = debug
        
        username = os.getenv("HUE_USERNAME")
        
        if not username:
            raise ValueError("Your HUE_USERNAME is not found in .env")
        
        self.username = username
        
        bridge_id = os.getenv("HUE_BRIDGE_ID")
        
        if not bridge_id:
            raise ValueError("Your HUE_BRIDGE_ID is not found in .env")
        
        self.bridge_id = bridge_id.lower()
        self._log("Bridge ID:", self.bridge_id)
        self.https = HueHTTPS(
            bridge_ip=self.bridge_ip,
            bridge_id=self.bridge_id,
            ca_bundle=str(CA_BUNDLE),
        )
        
        self._lights_cache = None
        self._lights_cache_time = 0
        self._v2_scenes_cache = None
        self._v2_scenes_cache_time = 0
        self._scenes_cache = None
        self._scenes_cache_time = 0
    
   # ------ Internal Helpers, when Superman needs help -------
   
    def _log(self, *args):
        if self.debug:
            print(f"[{time.strftime('%H:%M:%S')}]", "[HUEAPI]", *args)
   
      
    def _get(self, endpoint: str):
        self._log("GET", endpoint)
        
        return self.https.get(
            f"/api/{self.username}/{endpoint}"
        )
 
    
    def _get_v2(self, endpoint: str):
        self._log("GET V2", endpoint)

        return self.https.get(
            f"/clip/v2/{endpoint}",
            headers={
                "hue-application-key": self.username
            },
        )
    
    
    def _put(self, endpoint: str, payload: dict):
         self._log("PUT", endpoint, payload)
         
         data = self.https.put(
             f"/api/{self.username}/{endpoint}",
             payload=payload,
         )
         
         self._log("RESPONSE", data)
         
         return data
    
     
    def _invalidate_lights_cache(self):
        self._lights_cache = None
        self._lights_cache_time = 0
        
        
    def get_config(self):
        return self._get("config")
           
           
    #------- Public API'S  -------#
    
        
    def get_all_lights_state(self):
        now = time.time()
        if(
            self._lights_cache is not None 
            and (now - self._lights_cache_time) < LIGHT_CACHE_SECONDS
            ):
            return self._lights_cache
        data = self._get("lights")
        self._lights_cache = data
        self._lights_cache_time = now
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
        self._invalidate_lights_cache()
        
    
    def set_group_power(self, on: bool):
        payload = {
            "on": on,
        }
        
        self._put("groups/0/action", payload)
        self._invalidate_lights_cache()
        
    def set_group_brightness(self, bri: int):
        payload = {
            "bri": bri,
            "transitiontime": 1
        }
        
        self._put("groups/0/action", payload)
        self._invalidate_lights_cache()
            
            
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
            self._v2_scenes_cache is not None
            and (now - self._v2_scenes_cache_time) < 60
        ):
            self._log("Using V2 scenes cache")
            return self._v2_scenes_cache
        data = self._get_v2("resource/scene")
        self._v2_scenes_cache = data
        self._v2_scenes_cache_time = now
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
        self._invalidate_lights_cache()