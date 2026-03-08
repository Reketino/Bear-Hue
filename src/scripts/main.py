from api.hue_discovery import discover_bridge_ip
from api.hue_api import HueAPI
from services.hue_service import HueService
from ui.main_window import MainWindow

def main():
    
    bridge_ip = discover_bridge_ip()
    
    if bridge_ip is None:
        print("No Hue Bridge found on the network.")
        return
    
    hue_api = HueAPI(bridge_ip)
    
    hue_service = HueService(hue_api)
    
    app = MainWindow(hue_service)
    app.mainloop()
    
    
if __name__ == "__main__":
    main()
    
