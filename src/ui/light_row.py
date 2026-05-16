import customtkinter as ctk
from src.services.hue_service import HueService

class LightRow(ctk.CTkFrame):
    
    def __init__(self, master, hue_service: HueService, light_id: int, name: str):
        super().__init__(
            master,
            fg_color="#151A17",
            border_color="#22382D",
            border_width=1,
            corner_radius=12
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
            hover_color="#1D2E25",
            text_color="#E6F2EC",
            corner_radius=10,
            font=("Segoe UI", 14, "bold")
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
        
        self.status.pack(side="right", padx=(6, 14))
        
        self.brightness_bar = ctk.CTkProgressBar(
            self, 
            width=80,
            corner_radius=100,
            progress_color="#6BAF92",
            fg_color="#2A2A2A"
        )
        self.brightness_bar.pack(side="right", padx=(0, 10))
        self.brightness_bar.set(0)
        
        self.brightness_label = ctk.CTkLabel(
            self,
            text="0%",
            width=60,
            anchor="e",
            font=("Consolas", 13),
            text_color="#B7C9BE"
        )
        self.brightness_label.pack(side="right", padx=10)
        self.refresh_status()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        for widget in self.winfo_children():
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            
                  
    def _on_enter(self, _):
        self.configure(fg_color= "#151A17")
            
    def _on_leave(self, _):
        self.configure(fg_color= "#18201B")
        self.after(100, self.refresh_status)
                
    def toggle_light(self):
        self.hue_service.toggle(self.light_id)
        
   
        
    def refresh_status(self):
        new_state = self.hue_service.get_light_state(
            self.light_id
        )
        
        if new_state != getattr(self, "last_state", None):
            self.last_state = new_state
            color = "#6BAF92" if new_state else "#A94442"
            self.status.configure(
                text_color=color
            )
            
        brightness = self.hue_service.get_brightness(
            self.light_id
        )
        self.brightness_label.configure(
            text=f"{brightness:>3}%"
        )
        self.after(3000, self.refresh_status) 
        
        
        