import customtkinter as ctk
from src.services.hue_service import HueService

class LightRow(ctk.CTkFrame):
    
    def __init__(self, master, hue_service: HueService, light_id: int, name: str):
        super().__init__(
            master,
            fg_color="#18201B",
            corner_radius=12,
            )
        
        self.hue_service = hue_service
        self.light_id = light_id
        
        self.pack(fill="x",padx=10, pady=6)
        
        button = ctk.CTkButton(
            self,
            text=name,
            height=36,
            width=140,
            anchor="w",
            command=self.toggle_light,
            
            fg_color="transparent",
            hover_color="#22382D",
            text_color="#E6F2EC",
            corner_radius=10
        )
        button.pack(side="left", fill="x", expand=True, padx= 10)
        
        is_on = self.hue_service.get_light_state(light_id)   
        color = "#6BAF92" if is_on else "#A94442"
            
        self.status = ctk.CTkLabel(
            self, 
            text="●", 
            text_color=color, 
            font=("Arial", 18)
            )
        
        self.status.pack(side="right", padx=8)
        
        self.brightness_bar = ctk.CTkProgressBar(
            self, 
            width=80,
            progress_color="#E48825"
        )
        self.brightness_bar.pack(side="right", padx=10)
        self.brightness_bar.set(0)
        
        self.brightness_label = ctk.CTkLabel(
            self,
            text="0%",
            width=50,
            anchor="e"
        )
        self.brightness_label.pack(side="right", padx=10)
        self.refresh_status()
     
        
    def toggle_light(self):
        current_color = self.status.cget("text_color")
        is_on = current_color == "green"
        self.status.configure(text_color="yellow")
        new_is_on = not is_on
        new_color = "green" if new_is_on else "red"
        self.status.configure(text_color=new_color)
        self.hue_service.toggle(self.light_id)
   
        
    def refresh_status(self):
        is_on = self.hue_service.get_light_state(self.light_id)
        color = "green" if is_on else "red"
        self.status.configure(text_color=color)
        brightness = self.hue_service.get_brightness(self.light_id)
        self.brightness_label.configure(text=f"{brightness}%")
        self.after(1000, self.refresh_status) 
        
        
    def update_state(self, is_on: bool, brightness: int):
        color = "green" if is_on else "red"
        self.status.configure(text_color=color)
        self.brightness_label.configure(text=f"{brightness}%")
        self.brightness_bar.set(brightness / 100)
        
        
        