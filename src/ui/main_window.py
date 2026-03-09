import customtkinter as ctk # type: ignore
from src.services.hue_service import HueService

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() # type: ignore
        
        self.hue_service = hue_service
        
        self.title("Bear Hue")
        self.geometry("300x300")
        
        on_button = ctk.CTkButton(
            self,
            text="All Lights ON",
            command=self.turn_all_on
        )
        on_button.pack(pady=10)
        
        off_button = ctk.CTkButton(
            self,
            text="All Lights OFF",
            command=self.turn_all_off
        )
        off_button.pack(pady=10)
        
        lights = hue_service.get_lights()
        
        for light_id, name in lights.items():
            
            button:  ctk.CTkButton = ctk.CTkButton(
                self,
                text=name,
                command=lambda i=light_id: self.toggle_light(i)
            )
            
            button.pack(pady=10) # type: ignore
            
    def toggle_light(self, light_id: int):
        self.hue_service.toggle(light_id)
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
    