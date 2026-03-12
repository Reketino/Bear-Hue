import customtkinter as ctk
from src.services.hue_service import HueService

class LightRow(ctk.CTkFrame):
    
    def __init__(self, master, hue_service: HueService, light_id: int, name: str):
        super().__init__(master)
        
        self.hue_service = hue_service
        self.light_id = light_id
        
        self.pack(fill="x", pady=6)