import requests

def  discover_bridge_ip() -> str | None:
    try:
        data = requests.get("https://discovery.meethue.com", timeout=5).json()
        
        if data: 
            return data[0]["internalipaddress"]
        
    except Exception as e:
        print("Could not find Bear's Hue Bridge", e)
        
        return None

