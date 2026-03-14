import customtkinter as ctk

from src.services.hue_service import HueService
from src.ui.light_row import LightRow
from src.ui.controls_bar import ControlsBar
from src.ui.brightness_slider import BrightnessSlider

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() 
        
        self.hue_service = hue_service
        self.buttons = {}
        self.light_rows = {}
        
        self.title("Bear Hue")
        self.geometry("300x300")
        
        ControlsBar(self, self.turn_all_on, self.turn_all_off)
        
        self.brightness = BrightnessSlider(self, self.change_brightness)
        self.lights_container = ctk.CTkScrollableFrame(self)
        self.lights_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._build_lights()
        
        self.refresh_lights()
        self.refresh_brightness()
        
    def _build_lights(self):
        lights = self.hue_service.get_lights()
        for light_id, name in lights.items():
            row = LightRow(
            self.lights_container,
            self.hue_service,
            light_id,
            name
            )
            self.light_rows[light_id] = row
        
    def refresh_lights(self):
        states= self.hue_service.get_all_lights_state()
        for light_id, data in states.items():
            row = self.light_rows.get(light_id)
            if row:
                row.update_state(data["on"], data["brightness"])
        self.after(1000, self.refresh_lights)
                            
    def refresh_brightness(self):
        brightness = self.hue_service.get_average_brightness()
        self.brightness.slider.set(brightness)
        self.after(1000, self.refresh_brightness)
                  
    def change_brightness(self, value):
        self.hue_service.set_all_brightness(int(value))
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
        
    