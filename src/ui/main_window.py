from PIL import Image
import customtkinter as ctk

from src.services.hue_service import HueService
from src.ui.controls_bar import ControlsBar
from src.ui.brightness_slider import BrightnessSlider
from src.ui.lights_panel import LightsPanel
from src.ui.scenes_bar import ScenesBar
from src.utils.path_utils import resource_path

class MainWindow(ctk.CTk):
    
    def __init__(self, hue_service: HueService) -> None:
        super().__init__() 
        
        self.hue_service = hue_service
        self.bear_mode = False
        self.title("Bear Hue")
        self.geometry("400x500")
        self.minsize(300, 400)
        
        self.configure(fg_color="#181818")
        self.attributes("-alpha", 0.98)
        
        self.bg_layer = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.ui_layer = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.ui_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        img = Image.open(resource_path("src/assets/bearhue.png")).convert("RGBA")
        self.bear_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(400, 400)
        )
        
        self.bear_label = ctk.CTkLabel(
            self,
            image=self.bear_image,
            text=""
        )
        self.bear_label.place_forget()
        
        ControlsBar(
            self.ui_layer, 
            self.turn_all_on, 
            self.turn_all_off, 
            self.toggle_bear_mode
        ).pack(fill="x", padx=15, pady=(10, 5))
        
        ScenesBar(
            self.ui_layer,
            self.hue_service
        ).pack(fill="x", padx=15, pady=5)
        
        self.brightness = BrightnessSlider(
            self.ui_layer, 
            self.change_brightness
        )
        self.brightness.pack(fill="x", padx=15, pady=5)
        
        self.lights_panel = LightsPanel(
            self.ui_layer, 
            self.hue_service
        ) 
        self.lights_panel.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        
        self.refresh()
        
        self.bg_layer.lower()
        self.ui_layer.lift()
        
        
    def enable_bear_mode(self):
        self.configure(fg_color="#1B2A1F")
        self.brightness.slider.configure(
            progress_color="#A3B18A",
            button_color="#588157"
        ) 
        for row in self.lights_panel.light_rows.values():
            row.configure(fg_color="#292E1E")
        self.bear_label.place(relx=0.5, rely=1, anchor="center")
        self.bear_label.configure(fg_color="transparent")
        self.bear_label.lift(self.ui_layer)
      
            
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
        states = self.hue_service.get_all_light_state()
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
    
    def _set_background_image(self):
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width < 10 or height < 10:
            return
        
        img = Image.open(resource_path("src/assets/bearhue.png")).convert("RGBA")
        img = img.resize((width, height))
        img = img.point(lambda p: p * 0.5)
        
        self.bear_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            
        )
        
        
        
        
        
    