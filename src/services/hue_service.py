from src.api.hue_api import HueAPI

class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        self.hue_api = hue_api
        
        
    def get_lights(self):
        return self.hue_api.list_lights()
    
    
    def get_light_state(self, light_id: int) -> bool:
        return self.hue_api.get_light_state(light_id)
    
    
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