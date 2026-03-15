import customtkinter as ctk

from src.ui.light_row import LightRow
from src.services.hue_service import HueService

class LightsPanel(ctk.CTkScrollableFrame):
    
    def __init__(self, master, hue_service: HueService):
        super().__init__(master)
        
        self.hue_service = hue_service 
        self.light_rows = {}
        
        self.pack(fill="both", expand=True, padx=20, pady=10)
        
        lights = self.hue_service.get_lights()
        
        for light_id, name in lights.items():
            
            row = LightRow(
            self,
            self.hue_service,
            light_id,
            name
            )
            self.light_rows[light_id] = row
            
    def update_lights(self, states): 
        for light_id, data in states.items():
            
            row = self.light_rows.get(light_id)
            
            if row:
                row.update_state(data["on"], data["brightness"])
            
    
  