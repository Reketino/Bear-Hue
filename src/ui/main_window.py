import customtkinter as ctk

from src.services.hue_service import HueService
from src.settings.settings_manager import SettingsManager
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
        self.minsize(320, 420)
        

        self.configure(fg_color="#101010")
        
        
        self.ui_layer = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.ui_layer.pack(fill="both", expand=True)
        
            
        self.controls = ControlsBar(
            self.ui_layer, 
            self.turn_all_on, 
            self.turn_all_off, 
            self.toggle_bear_mode
        )
        self.controls.pack(fill="x", padx=15, pady=(10, 5))
        
        
        self.scenes = ScenesBar(
            self.ui_layer,
            self.hue_service
        )
        self.scenes.pack(fill="x", padx=15, pady=5)
        
        
        self.brightness = BrightnessSlider(
            self.ui_layer, 
            self.change_brightness
        )
        self.brightness.pack(fill="x", padx=15, pady=5)
        self._default_slider_style = {
            "progress_color": self.brightness.slider._progress_color,
            "button_color": self.brightness.slider._button_color,
            "button_hover_color": self.brightness.slider._button_hover_color,
            "fg_color": self.brightness.slider._fg_color,
        }
        
        self.lights_panel = LightsPanel(
            self.ui_layer, 
            self.hue_service
        ) 
        self.lights_panel.pack(
            fill="both", 
            expand=True, 
            padx=15, 
            pady=(5, 10)
        )
        
        self.default_theme()
        
        self.refresh()
        
    def default_theme(self):
        self.configure(fg_color="#101010")
        self.controls.glow.configure(fg_color="transparent")
        self.scenes.set_bear_mode(False)
        self.brightness.slider.configure(
            progress_color="#CFE6FD",
            button_color="#011120",
            button_hover_color="#A3BECC",
            fg_color="#4F4F4F",
            border_width=0
        )
        
        for row in self.lights_panel.light_rows.values():
            
            row.configure(
                fg_color="#17191D",
                border_color="#2B3138",
                border_width=1   
            )
            
            row.brightness_bar.configure(
                progress_color="#6BAF92",
                fg_color="#2A2A2A"
            )
            
    def enable_bear_mode(self):
        self.configure(fg_color="#0B0F0D")
        self.controls.bear_banner.grid()
        self.controls.glow.configure(
            fg_color="#1f3d2b"
        )
        self.scenes.set_bear_mode(True)
        bear_color = "#6BAF92"
        self.brightness.slider.configure(
            progress_color=bear_color,
            button_color="#506D06",
            button_hover_color= "#354A00"
        )
        for row in self.lights_panel.light_rows.values():
            row.set_bear_mode(True)
            row.configure(
                fg_color="#18201B",
                border_width=0
            )
            
            row.brightness_bar.configure(
                fg_color="#0E1310",
                progress_color="#6BAF92"
            )

          
    def disable_bear_mode(self):
        self.controls.bear_banner.grid_remove()
        for row in self.lights_panel.light_rows.values():
            row.set_bear_mode(False)
        self.default_theme()
        
        
    def toggle_bear_mode(self):
        self.bear_mode = not self.bear_mode
        if self.bear_mode:
            self.enable_bear_mode()
        else:
            self.disable_bear_mode()    
    
           
    def refresh(self):
        states = self.hue_service.get_all_light_state()
        self.lights_panel.update_lights(states)
        brightness = self.hue_service.get_average_brightness(states)
        if not self.brightness.is_dragging:
            current = int(self.brightness.slider.get())
            if abs(current - brightness) >= 1:
                self.brightness.slider.set(brightness)
        self.after(1000, self.refresh)
    
                                             
    def change_brightness(self, value):
        value = int(value)
        self.hue_service.set_all_brightness(value)
        if self.bear_mode:
            color = self._get_bear_color(value)
            self.brightness.slider.configure(
                progress_color=color,
                button_color=color
            )
            for row in self.lights_panel.light_rows.values():
                row.configure(border_color=color)
            soft_glow = "#1A221D"
            self.controls.glow.configure(fg_color=soft_glow)
               
    def turn_all_on(self):
        self.hue_service.turn_all_on()
        
    def turn_all_off(self):
        self.hue_service.turn_off_all()
        
    def _get_bear_color(self, value: int) -> str:
        intensity = int (40 + (value / 100) * 120)
        r = int(intensity * 0.3)
        g = intensity 
        b = int(intensity * 0.4)
        return f"#{r:02x}{g:02x}{b:02x}"
        
        
        