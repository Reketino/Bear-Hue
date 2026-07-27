import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]/"src"))

from src.api.hue_discovery import discover_bridge_ip
from src.api.hue_api import HueAPI


def run_test():
    
    bridge_ip = discover_bridge_ip()
    
    if not bridge_ip:
        print("We can't seem to find ur Hue Bridge on the network.")
        return
    
    hue = HueAPI(bridge_ip)
    
    
    # TEST 1: Lights
    lights = hue.list_lights()
    
    print("\nWe Found your lights:\n")
    
    for light_id, name in lights.items():
        print(f"{light_id}: {name}")
        
    
    # TEST 2: Scenes
    print("\nWe Found your scenes:\n")
    
    scenes = hue.get_scenes()
    
    for scene_id, data in scenes.items():
        name = data.get("name", "Unknown")
        print(f"{scene_id}: {name}")    
        
    # TEST 3: V2 Scene Gallery   
    print("\nWe Founde V2 Scenes:\n")
    
    v2_scenes = hue.get_v2_scenes()
    
    for scene in v2_scenes.get("data", []):
        
        print(
            "\n---",
            scene["metadata"]["name"],
            "---"
        )
        
        print(
            scene["palette"]
        )
        
        break
    
    # TEST 4: Bridge Config
    config = hue.get_config()
    
    print("\nBridge ID:")
    print(config.get("bridgeid"))
    
    
    
        
# Run script w/ python -m tests.test_api
if __name__ == "__main__":
    run_test()
    
    