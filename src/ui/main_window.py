from PIL import Image
import customtkinter as ctk

from src.services.hue_service import HueService
from src.ui.controls_bar import ControlsBar
from src.ui.brightness_slider import BrightnessSlider
from src.ui.lights_panel import LightsPanel
from src.ui.scenes_bar import ScenesBar

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() 
        
        self.hue_service = hue_service
        self.bear_mode = False
        self.title("Bear Hue")
        self.geometry("400x500")
        self.minsize(300, 400)
        
        self.bg_layer = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.ui_layer = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.bear_image = ctk.CTkImage(
            light_image=Image.open("src/assets/bearhue.png"),
            dark_image=Image.open("src/assets/bearhue.png"),
            size=(800, 800)
        )
        
        self.bear_label = ctk.CTkLabel(
            self.bg_layer,
            image=self.bear_image,
            text=""
        )
        self.bear_label.place_forget()
        
        ControlsBar(
            self, 
            self.turn_all_on, 
            self.turn_all_off, 
            self.toggle_bear_mode
            )
        
        ScenesBar(
            self,
            self.scene_movie,
            self.scene_relax,
            self.scene_bright
        )
        
        self.brightness = BrightnessSlider(self, self.change_brightness)
        self.lights_panel = LightsPanel(self, self.hue_service)
        self.refresh()
        
        self.bg_layer.lower()
    
    def enable_bear_mode(self):
        self.configure(fg_color="#1B2A1F")
        self.brightness.slider.configure(
            progress_color="#A3B18A",
            button_color="#588157"
        ) 
        for row in self.lights_panel.light_rows.values():
            row.configure(fg_color="#2D3E2F")
        self.bear_label.place(relx=0, rely=0, relwidth=1, relheight=1)
      
            
    def disable_bear_mode(self):
        self.configure(fg_color="#1E1E1E")
        self.brightness.slider.configure(
            progress_color="#FFD54F",
            button_color="#FFC107"
        ) 
        for row in self.lights_panel.light_rows.values():
            row.configure(fg_color="#2B2B2B") 
        self.bear_label.place_forget()
        
    def toggle_bear_mode(self):
        self.bear_mode = not self.bear_mode
        if self.bear_mode:
            self.enable_bear_mode()
        else:
            self.disable_bear_mode()    
    
           
    def refresh(self):
        states= self.hue_service.get_all_lights_state()
        self.lights_panel.update_lights(states)
        brightness = self.hue_service.get_average_brightness()
        self.brightness.slider.set(brightness)
        self.after(500, self.refresh)
    
                                             
    def change_brightness(self, value):
        self.hue_service.set_all_brightness(int(value))
               
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
    def scene_movie(self):
        self.hue_service.set_scene("movie")
        
    def scene_relax(self):
        self.hue_service.set_scene("relax")
        
    def scene_bright(self):
        self.hue_service.set_scene("bright")
        
        
    