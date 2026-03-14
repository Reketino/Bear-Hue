from src.api.hue_api import HueAPI
import time

class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        
        self.hue_api = hue_api
        
        self._lights_cache = None
        self._cache_time = 0 
        
    def get_lights(self):
        return self.hue_api.list_lights()
    
    
    def get_light_state(self, light_id: int) -> bool:
        return self.hue_api.get_light_state(light_id)
    
    
    def get_all_lights_state(self):
        lights = self._get_lights_cached()
        result = {}
        for light_id, data in lights.items():
            result[int(light_id)] = {
                "on": data["state"]["on"],
                "brightness": int(data["state"]["bri"] / 2.54)
            }
        return result
    
    
    def _get_lights_cached(self):
        now = time.time()
        if self._lights_cache and (now - self._cache_time) < 0.5:
            return self._lights_cache
        lights = self.hue_api.get_all_lights_state()
        self._lights_cache = lights
        self._cache_time = now
        return lights
        

    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
      
        
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)
        
        
    def toggle(self, light_id: int):
        is_on = self.hue_api.get_light_state(light_id)
        self.hue_api.set_light(light_id, not is_on)
    
        
    def turn_all_on(self):
        lights = self.hue_api.list_lights()
        for light_id in lights.keys():
            self.hue_api.set_light(light_id, True)
      
            
    def turn_off_all(self):
        lights = self.hue_api.list_lights()
        for light_id in lights.keys():
            self.hue_api.set_light(light_id, False)
            
    
    def get_brightness(self, light_id: int) -> int:
        bri = self.hue_api.get_brightness(light_id)
        return int(bri / 2.54)
    
    
    def get_average_brightness(self) -> int:
        lights = self._get_lights_cached()
        values = [
            data["state"]["bri"]
            for data in lights.values() 
        ]
        if not values:
            return 0
        avg = sum(values) / len(values)
        return int(avg / 2.54)
            
    
    def set_all_brightness(self, value: int):
        lights = self.hue_api.list_lights()
        bri = int(value * 2.54)
        for light_id in lights.keys():
            self.hue_api.set_brightness(light_id, bri)