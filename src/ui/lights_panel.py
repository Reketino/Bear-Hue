import customtkinter as ctk

from src.ui.light_row import LightRow
from src.services.hue_service import HueService

class LightsPanel(ctk.CTkScrollableFrame):
    
    def __init__(self, master, hue_service: HueService):
        super().__init__(master)
        
        self.hue_service = hue_service 
        self.light_rows = {}