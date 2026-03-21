from src.api.hue_api import HueAPI
import time

class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        self.hue_api = hue_api
        
      
    def get_lights(self):
        return self.hue_api.list_lights()
    
    
    def get_all_light_state(self):
        lights = self.hue_api.get_all_lights_state()
        
        return {
            int(light_id): {
                "on": data["state"]["on"],
                "brightness": int(data["state"]["bri"]/ 2.54)
            }
            for light_id, data in lights.items()
        }
    
    
    def get_lights_state(self, light_id: int) -> bool:
       lights = self.hue_api.get_all_lights_state()
       return lights[str(light_id)]["state"]["on"]
   
    def get_brightness(self, light_id: int) -> int:
        lights = self.hue_api.get_all_lights_state()
        bri = lights[str(light_id)]["state"]["bri"]
        return int(bri / 2.54)   
    
    def get_average_brightness(self) -> int:
        lights = self.hue_api.get_all_lights_state()
        values = [
            data["state"]["bri"]
            for data in lights.values() 
        ]
        if not values:
            return 0
        avg = sum(values) / len(values)
        return int(avg / 2.54)

    
    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
      
        
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)
        
        
    def toggle(self, light_id: int):
        is_on = self.get_light_state(light_id)
        self.hue_api.set_light(light_id, not is_on)
        self._invalidate_cache()
    
        
    def turn_all_on(self):
        lights = self._get_lights_cached()
        for light_id in lights.keys():
            self.hue_api.set_light(light_id, True)
        self._invalidate_cache()
      
            
    def turn_off_all(self):
        lights = self.hue_api.list_lights()
        for light_id in lights.keys():
            self.hue_api.set_light(light_id, False)
            
    

    
    
   
            
    
    def set_all_brightness(self, value: int):
        lights = self._get_lights_cached()
        bri = int(value * 2.54)
        for light_id in lights.keys():
            self.hue_api.set_brightness(int(light_id), bri)
            self._invalidate_cache()
            
            
    def set_scene(self, scene: str):
        scenes = {
            "movie": 30,
            "relax": 60,
            "bright": 100
        }
        brightness = scenes.get(scene)
        if brightness is None:
            return
        self.set_all_brightness(brightness)
    
    
    def _invalidate_cache(self):
        self._lights_cache = None
        self._cache_time = 0