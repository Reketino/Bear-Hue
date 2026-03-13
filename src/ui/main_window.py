import customtkinter as ctk 
from src.services.hue_service import HueService
from src.ui.light_row import LightRow

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() 
        
        self.hue_service = hue_service
        self.buttons = {}
        
        self.title("Bear Hue")
        self.geometry("300x300")
        
        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=20, pady=20)
        
        
        on_button = ctk.CTkButton(
            controls,
            text="All Lights ON",
            command=self.turn_all_on
        )
        on_button.pack(side="left", padx=10)
        
        off_button = ctk.CTkButton(
            controls,
            text="All Lights OFF",
            command=self.turn_all_off
        )
        off_button.pack(side="right", padx=5)
        
              
        brightness_label = ctk.CTkLabel(
            self, 
            text="Brightness"
            )
        brightness_label.pack(
            pady=(10, 0)
            )
        
        self.brightness_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.change_brightness
        )
        
        self.brightness_slider.set(100)
        self.brightness_slider.pack(fill="x", padx=30, pady=10)
        
        
        lights_container = ctk.CTkScrollableFrame(self)
        lights_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        
        lights = hue_service.get_lights()
        
        for light_id, name in lights.items():
            
            LightRow(
                lights_container,
                self.hue_service,
                light_id,
                name
            )
                        
    def refresh_brightness(self):
        brightness = self.hue_service.get_average_brightness()
        self.brightness_slider.set(brightness)
        self.after(1000, self.refresh_brightness)
                  
    def change_brightness(self, value):
        self.hue_service.set_all_brightness(int(value))
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
        
    