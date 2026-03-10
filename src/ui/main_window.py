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
        
        self.status_labels = {}
        
        for light_id, name in lights.items():
            
            row = ctk.CTkFrame(self)
            row.pack(fill="x", padx=20, pady=5)
            
            button:  ctk.CTkButton = ctk.CTkButton(
                self,
                text=name,
                command=lambda i=light_id: self.toggle_light(i)
            )
            
            button.pack(pady=5) # type: ignore
            
            is_on = self.hue_service.get_light_state(light_id)
            
            color = "green" if is_on else "red"
            
            label = ctk.CTkLabel(self, text="●", text_color=color)
            label.pack()
            
            self.buttons[light_id] = (button, name)
            self.status_labels[light_id] = label
            
    def toggle_light(self, light_id: int):
        
        self.hue_service.toggle(light_id)
        
        is_on = self.hue_service.get_light_state(light_id)
        
        color = "green" if is_on else "red"
        
        label = self.status_labels[light_id]
        
        label.configure(text_color=color) 
        
    def refresh_status(self):
        
        for light_id, label in self.status_labels.items():
            
            is_on = self.hue_service.get_light_state(light_id)
            
            color = "green" if is_on else "red"
            
            label.configure(text_color=color)
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        self.refresh_status()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        self.refresh_status()
        
    