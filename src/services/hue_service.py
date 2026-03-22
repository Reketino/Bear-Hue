from src.api.hue_api import HueAPI


class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        self.hue_api = hue_api
        
    # -------- READ Lights Logic --------
         
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
   
     # -------- READ Brightness Logic --------
   
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
    
      # -------- READ Scenes Logic --------
    
    def get_scenes(self):
        scenes = self.hue_api.get_scenes()
        result = []
        for scene_id, data in scenes.items():
            if data.get("type") != "GroupScene":
                continue
            result.append({
                "id": scene_id,
                "name": data["name"]
            })
        return sorted(result, key=lambda x: x["name"])
    
    
    # -------- WRITE LOGIC --------
    
    
    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
         
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)
           
    def toggle(self, light_id: int):
        is_on = self.get_lights_state(light_id)
        self.hue_api.set_light(light_id, not is_on)
         
    def turn_all_on(self):
        lights = self.hue_api.get_all_lights_state()
        for light_id in lights.keys():
            self.hue_api.set_light(int(light_id), True)
              
    def turn_off_all(self):
        lights = self.hue_api.get_all_lights_state()
        for light_id in lights.keys():
            self.hue_api.set_light(int(light_id), False)
        
    def set_all_brightness(self, value: int):
        bri = int(value * 2.54)
        lights = self.hue_api.get_all_lights_state()
        for light_id in lights.keys():
            self.hue_api.set_brightness(int(light_id), bri)
       
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
    