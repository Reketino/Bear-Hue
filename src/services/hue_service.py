from src.api.hue_api import HueAPI


class HueService: 
    
    def __init__(self, hue_api: HueAPI):
        self.hue_api = hue_api
    
        
    # -------- INTERNAL HELPERS --------  
        
    def _get_lights(self):
       return self.hue_api.get_all_lights_state()
   
    def _hue_to_hex(self, hue, sat, bri):
        import colorsys
        h = hue / 65536
        s = sat / 254
        v = bri / 254
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return "#{:02x}{:02x}{:02x}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255),
        )
        

    # -------- READ Lights Logic --------
         
    def get_lights(self):
        return self.hue_api.list_lights()
    
    def get_all_light_state(self):
        lights = self._get_lights()
        
        return {
            int(light_id): {
                "on": data["state"]["on"],
                "brightness": int(data["state"]["bri"]/ 2.54)
            }
            for light_id, data in lights.items()
        }
    
    def get_light_state(self, light_id: int) -> bool:
       lights = self._get_lights()
       return lights[str(light_id)]["state"]["on"]
   
   
     # -------- READ Brightness Logic --------
   
    def get_brightness(self, light_id: int) -> int:
        lights = self._get_lights()
        bri = lights[str(light_id)]["state"]["bri"]
        return int(bri / 2.54)   
   
    def get_average_brightness(self) -> int:
        lights = self._get_lights()
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
    
    def get_scene_color(self, scene_id: str):
        scene = self.hue_api.get_scene(scene_id)
        if not scene:
            return "#888888"
        if isinstance(scene, list):
            scene = scene[0]
        lights = scene.get("lightstates")
        if lights:
            first = next(iter(lights.values()))
        hue = first.get("hue", 0)
        sat = first.get("sat", 0)
        bri = first.get("bri", 254)
        if hue is not None or sat is not None or bri is not None:
            return self._hue_to_hex(hue, sat, bri)
        all_lights = self._get_lights()
        for light in all_lights.values():
            state = light.get("state", {})
            if state.get("on"):
                
    
    
    # -------- WRITE ON/OFF LOGIC --------
    
    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
         
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)
           
    def toggle(self, light_id: int):
        is_on = self.get_light_state(light_id)
        self.hue_api.set_light(light_id, not is_on)
         
    def turn_all_on(self):
        lights = self._get_lights()
        for light_id in lights.keys():
            self.hue_api.set_light(int(light_id), True)
              
    def turn_off_all(self):
        lights = self._get_lights()
        for light_id in lights.keys():
            self.hue_api.set_light(int(light_id), False)
            
    # -------- WRITE BRIGHTNESS LOGIC --------
        
    def set_all_brightness(self, value: int):
        bri = int(value * 2.54)
        lights = self._get_lights()
        for light_id in lights.keys():
            self.hue_api.set_brightness(int(light_id), bri)
            
    # -------- WRITE SCENE LOGIC --------
    
    def activate_scene(self, scene_id: str):
        self.hue_api.activate_scene(scene_id)
        
    def activate_scene_by_name(self, name: str):
        scenes = self.get_scenes()
        for scene in scenes:
            if scene["name"].lower() == name.lower():
                self.hue_api.activate_scene(scene["id"])
                return
            print(f"Scene '{name}' not found")
            
    
            
       
 