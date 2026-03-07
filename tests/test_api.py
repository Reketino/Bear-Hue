from api.hue_discovery import discover_bridge_ip
from api.hue_api import HueAPI

def run_test():
    
    bridge_ip = discover_bridge_ip()
    
    if not bridge_ip:
        print("We can't seem to find ur Hue Bridge on the network.")
        return
    
    hue = HueAPI(bridge_ip)
    
    lights = hue.get_lights()
    
    print("\nWe Found your lights:\n")
    
    for light_id, light in lights.items():
        print(f"{light_id}: {light['name']}")
        

# Run script w/ python -m tests.test_api
if __name__ == "__main__":
    run_test()
    
    