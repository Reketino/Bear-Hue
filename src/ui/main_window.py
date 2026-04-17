import tkinter as tk
from PIL import Image, ImageTk
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
        
        self.configure(fg_color="#101010")
        
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.ui_layer = ctk.CTkFrame(self, fg_color="#000000")
        self.ui_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # self.overlay = ctk.CTkFrame(self, fg_color="#111111")
        # self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
            
        self.ui_layer.lift()
      
        self.controls = ControlsBar(
            self.ui_layer, 
            self.turn_all_on, 
            self.turn_all_off, 
            self.toggle_bear_mode
        )
        self.controls.pack(fill="x", padx=15, pady=(10, 5))
        
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
            
    def enable_bear_mode(self):
        self.update_idletasks()
        self.after(100,self._activate_bear_mode)
        
        
    def _activate_bear_mode(self):
        self._set_background_image()
        self.ui_layer.lift()
        self.configure(fg_color="#000000")
        self.controls.bear_banner.grid()
        self.controls.glow.configure(fg_color="#1f3d2b")
        self.brightness.show_bear()
        self.brightness.slider.configure(
            progress_color="#A3B18A",
            button_color="#588157"
        ) 
        for row in self.lights_panel.light_rows.values():
            row.configure(fg_color="#292E1E")

          
    def disable_bear_mode(self):
        self.canvas.delete("all")
        self.configure(fg_color="#101010")
        self.controls.bear_banner.grid_remove()
        self.controls.glow.configure(fg_color="transparent")
        self.brightness.hide_bear()
        self.brightness.slider.configure(
            progress_color="#FFD54F",
            button_color="#FFC107"
        ) 
        for row in self.lights_panel.light_rows.values():
            row.configure(fg_color="#2B2B2B") 
        
        
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
        if not self.brightness.is_dragging:
            self.brightness.slider.set(brightness)
        self.after(500, self.refresh)
    
                                             
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
                row.configure(fg_color=color)
            self.controls.glow.configure()
               
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
        
    
    def _set_background_image(self):
        width = self.winfo_width()
        height = self.winfo_height()
        if width < 10 or height < 10:
            return
        img = Image.open(resource_path("src/assets/bearhue.png")).convert("RGBA")
        img = img.resize((width, height))
        r, g, b, a = img.split()
        r = r.point(lambda p: p * 0.8)
        g = g.point(lambda p: p * 0.8)
        b = b.point(lambda p: p * 0.8)
        img= Image.merge("RGBA", (r, g, b, a))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        print("SIZE:", width, height)
        
        
        