import customtkinter as ctk # type: ignore
import time
from src.services.hue_service import HueService

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() # type: ignore
        
        self.hue_service = hue_service
        self.buttons = {}
        
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
            
            is_on = self.hue_service.get_light_state(light_id)
            
            status = "🟢" if is_on else "🔴"
            
            button:  ctk.CTkButton = ctk.CTkButton(
                self,
                text=f"{name} {status}",
                command=lambda i=light_id: self.toggle_light(i)
            )
            
            button.pack(pady=10) # type: ignore
            
            self.buttons[light_id] = (button, name)
            
    def toggle_light(self, light_id: int):
        self.hue_service.toggle(light_id)
        
        time.sleep(0.2)
        
        is_on = self.hue_service.get_light_state(light_id)
        
        status = "🟢" if is_on else "🔴"
        
        button, name = self.buttons[light_id]
        
        button.configure(text=f"{name} {status}")
        
    def refresh_status(self):
        for light_id, (button, name) in self.buttons.items():
            
            time.sleep(0.2)
            
            is_on = self.hue_service.get_light_state(light_id)
            
            status = "🟢" if is_on else "🔴"
            
            button.configure(text=f"{name} {status}")
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        self.refresh_status()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        self.refresh_status()
        
    