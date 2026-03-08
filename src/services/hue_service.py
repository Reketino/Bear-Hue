from src.api.hue_api import HueAPI

class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        self.hue_api = hue_api
        
    def get_lights(self):
        return self.hue_api.list_lights()
    
    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
        
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)