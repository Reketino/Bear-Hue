import customtkinter as ctk

class BrightnessSlider(ctk.CTkFrame):
    
    def __init__(self, master, command):
        super().__init__(master)
        
        self.external_command = command
        
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
        self.bear_icon.place(relx=0.0, rely=0.5, anchor="center")
        self.bear_icon.place_forget()
        
    def _on_slide(self, value):
        if hasattr(self,"bear_icon"):
            self.bear_icon.place(relx=float(value)/100, rely=0.65, anchor="center")
        if self.external_command:
            self.external_command(value)
            
    def show_bear(self):
        self.bear_icon.place(relx=self.slider.get()/100, rely=0.65, anchor="center")
        
        