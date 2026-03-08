import customtkinter as ctk # type: ignore
from services.hue_service import HueService

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() # type: ignore
        
        self.hue_service = hue_service
        
        self.title("Bear Hue")
        self.geometry("300x300")
        
        lights = hue_service.get_lights()
        
        for light_id, name in lights.items():
            
            button:  ctk.CTkButton = ctk.CTkButton(
                self,
                text=name,
                command=lambda i=light_id: self.toggle_light(i)
            )
            
            button.pack(pady=10) # type: ignore
            
    def toggle_light(self, light_id: str):
        self.hue_service.turn_on(int(light_id))