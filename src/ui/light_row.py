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
            
        self.status = ctk.CTkLabel(
            self, 
            text="●", 
            text_color=color, 
            font=("Arial", 18)
            )
        
        self.status.pack(side="right", padx=8)
        
       
        
        self.brightness_label = ctk.CTkLabel(
            self,
            text="0%",
            width=50,
            anchor="e"
        )
        self.brightness_label.pack(side="right", padx=10)
        
        self.refresh_status()
     
        
    def toggle_light(self):
        self.hue_service.toggle(self.light_id)
   
        
    def refresh_status(self):
        is_on = self.hue_service.get_light_state(self.light_id)
        color = "green" if is_on else "red"
        self.status.configure(text_color=color)
        brightness = self.hue_service.get_brightness(self.light_id)
        self.brightness_label.configure(text=f"{brightness}%")
        self.after(1000, self.refresh_status) 
        
        
        