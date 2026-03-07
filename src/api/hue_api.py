import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HueAPI:
    
    def __init__(self, bridge_ip: str):
        
        self.bridge_ip = bridge_ip
        self.username = os.getenv("HUE_USERNAME")
        
        if not self.username:
            raise ValueError("Your HUE_USERNAME is not found in .env")
        
        self.base_url = f"http://{self.bridge_ip}/api/{self.username}"
    