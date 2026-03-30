from src.api.hue_api import HueAPI
from src.utils.color_utils import hue_to_hex, xy_to_hex, ct_to_hex


class HueService: 
    
    def __init__(self, hue_api: HueAPI, debug: bool = False):
        self.hue_api = hue_api
        self.debug = debug
    
        
    # -------- INTERNAL HELPERS --------  
        
    def _get_lights(self):
       return self.hue_api.get_all_lights_state()
   
    def _log(self, *args):
        if self.debug:
            print(*args)
   
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
        
    def _xy_to_hex(self, x, y, bri):
        z = 1.0 - x - y
        Y = bri / 254
        if y == 0:
            return "#888888"
        X = (Y / y) * x
        Z = (Y / y) * z
        r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
        b = X * 0.051713 - Y * 0.121364 + Z * 1.011530
        r = max(0, r)
        g = max(0, g)
        b = max(0, b)
        return "#{:02x}{:02x}{:02x}".format(
            int (min(r * 255, 255)),
            int (min(g * 255, 255)),
            int (min(b * 255, 255)),
        )
        
    def _ct_to_hex(self, ct, bri):
        ratio = (ct - 153) / (500 - 153)
        r = int(255 * (1 - ratio * 0.3))
        g = int(244 * (1 - ratio * 0.2))
        b = int(255 * (1 - ratio))
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
        
        
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
            self._log("No scene found:", scene_id)
            return "#888888"
        
        if isinstance(scene, list):
            scene = scene[0]
            
        self._log("RAW SCENE:", scene_id, scene)
        lights = scene.get("lightstates")
        if lights:
            first = next(iter(lights.values()))
            
            hue = first.get("hue")
            sat = first.get("sat")
            bri = first.get("bri", 254)
            self._log("SCENE DATA:", scene_id, "->", hue, sat, bri)
            if hue is not None and sat is not None:
                hex_color = hue_to_hex(hue, sat, bri)
                self._log("USING HSV:", hex_color)
                return hex_color
            
            xy = first.get("xy")
            if xy:
                hex_color = xy_to_hex(xy[0], xy[1], bri)
                self._log("USING XY:", hex_color)
                return hex_color
            
            ct = first.get("ct")
            if ct:
                hex_color = ct_to_hex(ct, bri)
                self._log("USING CT:", hex_color)
                return hex_color
            
        self._log("FALLBACK triggered for scene:", scene_id)
       
        all_lights = self._get_lights()
        for light_id, light in all_lights.items():
            state = light.get("state", {})
           
            if state.get("on"):
                hue = state.get("hue")
                sat = state.get("sat")
                bri = state.get("bri")
                
                if hue is not None and sat is not None and bri is not None:
                    hex_color = hue_to_hex(hue, sat, bri)
                    self._log(f"USING LIGHT{light_id} COLOR:", hex_color)
                    return hex_color
        self._log("NO COLOR FOUND -> returning to default")
        return "#888888"    
                
                
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
                self.activate_scene(scene["id"])
                return
        self._log(f"Scene '{name}' not found")
            
    
            
       
 