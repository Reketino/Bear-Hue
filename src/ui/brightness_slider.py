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
            command=self._on_slide
        )
        self.slider.pack(fill="x", padx=10, pady=10)
        
        self.bear_icon = ctk.CTkLabel(
            self,
            text="🐻",
            font=("Segoe UI Emoji", 20)
        )
        self.bear_icon.place(relx=0.0, rely=0.5, anchor="center")
        self.bear_icon.place_forget()
        
    def _on_slide(self, value):
            slider_width = self.slider.winfo_width()
            if slider_width > 1:
               x = 10 + (float(value) / 100) * (slider_width - 20)
               self.bear_icon.place(x=x, rely=0.65, anchor="center")
            if self.external_command:
                self.external_command(value)
            
    def show_bear(self):
        self.bear_icon.place(rely=0.65, anchor="center")
        self.after(50, lambda: self._on_slide(self.slider.get()))
            
    def hide_bear(self):
        self.bear_icon.place_forget()
        
        