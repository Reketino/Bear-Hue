import customtkinter as ctk

from src.services.hue_service import HueService
from src.ui.light_row import LightRow
from src.ui.controls_bar import ControlsBar
from src.ui.brightness_slider import BrightnessSlider
from src.ui.lights_panel import LightsPanel

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
        self.lights_panel = LightsPanel(self, self.hue_service)
        self.refresh()
       
        
    def refresh(self):
        states= self.hue_service.get_all_lights_state()
        self.lights_panel.update_lights(states)
        brightness = self.hue_service.get_average_brightness()
        self.brightness.slider.set(brightness)
        self.after(1000, self.refresh)
                                             
    def change_brightness(self, value):
        self.hue_service.set_all_brightness(int(value))
        
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
        
    