import customtkinter as ctk
from src.services.hue_service import HueService

class LightRow(ctk.CTkFrame):
    
    def __init__(self, master, hue_service: HueService, light_id: int, name: str):
        super().__init__(master)
        
        self.hue_service = hue_service
        self.light_id = light_id
        
        self.pack(fill="x", pady=6)
        
        button = ctk.CTkButton(
            self,
            text=name,
            height=40,
            anchor="w",
            command=self.toggle_light
        )
        
        button.pack(side="left", fill="x", expand=True, padx= 10)
        
        is_on = self.hue_service.get_light_state(light_id)
            
        color = "green" if is_on else "red"
            
        label = ctk.CTkLabel(
            row, 
            text="●", 
            text_color=color, 
            font=("Arial", 18)
            )
        label.pack(side="right", padx=15)
        
        