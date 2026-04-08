import customtkinter as ctk

class BrightnessSlider(ctk.CTkFrame):
    
    def __init__(self, master, command):
        super().__init__(master)
        
        self.pack(fill="x", padx=20, pady=20)
        
        label = ctk.CTkLabel(self, text="Brightness")
        label.pack(pady=(0, 5))
        
        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            number_of_steps=100,
            command=command
        )
        self.slider.pack(fill="x", padx=10, pady=10)
        
        self.bear_icon = ctk.CTkLabel(
            self,
            text="🐻",
            font=("Segoe UI Emoji", 16)
        )