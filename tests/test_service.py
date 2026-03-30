from src.api.hue_api import HueAPI
from src.services.hue_service import HueService
from src.api.hue_discovery import discover_bridge_ip

def main():
    bridge_ip = discover_bridge_ip()
    if not bridge_ip:
        print("No Hue Bridge found")
        return
    api = HueAPI(bridge_ip)
    service = HueService(api, debug=True)
    
    print ("\n--- SCENES ---")
    scenes = service.get_scenes()
    for scene in scenes:
        print(scene)
        
    print ("\n--- SCENE COLORS ---")
    for scene in scenes:
        color = service.get_scene_color(scene["id"])
        print(scene["name"], "->", color)
        
    print ("\n--- ACTIVATE TEST ---")
    if scenes:
        first = scenes[0]
        print("Activating:", first["name"])
        service.activate_scene(first["id"])
 
        
if __name__ == "__main__":
    main()