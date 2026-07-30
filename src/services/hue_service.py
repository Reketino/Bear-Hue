from src.api.hue_api import HueAPI
from src.utils.color_utils import hue_to_hex, xy_to_hex, ct_to_hex


class HueService: 
    
    def __init__(self, hue_api: HueAPI, debug: bool = False):
        self.hue_api = hue_api
        self.debug = debug
        self._scene_palette_cache = {}
    
        
    # -------- INTERNAL HELPERS --------  
        
    def _get_lights(self):
       return self.hue_api.get_all_lights_state()
   
    def _log(self, *args):
        if self.debug:
            print(*args)
   
                           
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
   
      
    def get_average_brightness(
        self,
        states: dict[int, dict] | None = None,
        ) -> int:
        if states is None:
            states = self.get_all_light_state()
            
        values = [
            data["brightness"]
            for data in states.values() 
        ]
        if not values:
            return 0
        
        return round(sum(values) / len(values))
    
    
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
            if not first:
                return "#888888"
            
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
    
    
    def get_scene_palette(
        self,
        scene_name: str  
    ):
        if scene_name in self._scene_palette_cache:
            return self._scene_palette_cache[scene_name]
    
        scenes = self.hue_api.get_v2_scenes()
        for scene in scenes["data"]:
            if (
                scene["metadata"]["name"]
                != scene_name
            ):
                continue
            
            colors = []
            
            for item in scene["palette"].get(
                "color",
                []
            ):
                xy = item["color"]["xy"]
                
                colors.append(
                    xy_to_hex(
                        xy["x"],
                        xy["y"],
                        255
                    )
                )  
                
            self._scene_palette_cache[scene_name] = colors
            return colors
        self._scene_palette_cache[scene_name] = []
        return []
    
    
    def get_gallery_scene(self):
        scenes = self.hue_api.get_v2_scenes()
        result = []
        for scene in scenes.get("data", []):
            metadata = scene.get("metadata", {})
            palette = scene.get("palette", {})
            colors = palette.get("color", [])
            preview_color = "#888888"
            
            if colors:
                xy = colors[0]["xy"]
                preview_color = xy_to_hex(
                    xy["x"],
                    xy["y"],
                    255
                )
                
            result.append({
                "id": scene["id"],
                "name": metadata.get("name", "unknown"),
                "image": metadata.get("image"),
                "color": preview_color
            }) 
            
        return result
                
                
    # -------- WRITE ON/OFF LOGIC --------
    
    def turn_on(self, light_id: int):
        self.hue_api.set_light(light_id, True)
         
    def turn_off(self, light_id: int):
        self.hue_api.set_light(light_id, False)
           
    def toggle(self, light_id: int):
        is_on = self.get_light_state(light_id)
        self.hue_api.set_light(light_id, not is_on)
         
    def turn_all_on(self):
        self.hue_api.set_group_power(True)
              
    def turn_off_all(self):
        self.hue_api.set_group_power(False)
            
    # -------- WRITE BRIGHTNESS LOGIC --------
        
    def set_all_brightness(self, value: int):
        value = max(0, min(100, value))
        bri = round(value * 2.54)
        
        self.hue_api.set_group_brightness(bri)
            
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
            
    
            
       
 