from src.api.hue_discovery import discover_bridge_ip
from src.api.hue_api import HueAPI
from src.services.hue_service import HueService
from src.ui.main_window import MainWindow

def main():
    
    bridge_ip = discover_bridge_ip()
    
    if bridge_ip is None:
        print("No Hue Bridge found on the network.")
        return
    
    hue_api = HueAPI(bridge_ip)
    
    hue_service = HueService(hue_api)
    
    app = MainWindow(hue_service)
    app.mainloop()
    
# Run script w/: python -m src.scripts.main      
if __name__ == "__main__":
    main()
    
