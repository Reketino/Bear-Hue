from api.hue_discovery import discover_bridge_ip
from api.hue_api import HueAPI

def main():
    
    bridge_ip = discover_bridge_ip()
    
    if bridge_ip is None:
        print("No Hue Bridge found on the network.")
        return
    
    hue = HueAPI(bridge_ip)
    
    lights = hue.get_lights()
    
    print(lights)
    
if __name__ == "__main__":
    main()
    
