import customtkinter as ctk

class BrightnessSlider(ctk.CTkFrame):
    
    def __init__(self, master, command):
        super().__init__(master)
        
        self.external_command = command
        self.is_dragging = False
        
        self.pack(fill="x", padx=20, pady=20)
        
        label = ctk.CTkLabel(self, text="Brightness")
        label.pack(pady=(0, 5))
        
        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self._on_slide,
            button_color="#101010",
            button_hover_color="#101010",
        )
        self.slider.pack(fill="x", padx=10, pady=10)
        self.slider.bind("<ButtonPress-1>", self._start_drag)
        self.slider.bind("<ButtonRelease-1>", self._stop_drag)
        
        self.bear_icon = ctk.CTkLabel(
            self,
            text="🐻",
            font=("Segoe UI Emoji", 22)
        )
        self.bear_icon.place(relx=0.0, rely=0.5, anchor="center")
        self.bear_icon.place_forget()
        
    def _on_slide(self, value):
            slider_width = self.slider.winfo_width()
            if slider_width > 1:
                knob_offset = 12
                x = knob_offset + (float(value) / 100) * (slider_width - knob_offset * 2)
                self.bear_icon.place(in_=self.slider, x=x, rely=0.5, anchor="center")
                if self.external_command:
                   self.external_command(value)
               
            
    def show_bear(self):
        value = self.slider.get()
        slider_width = self.slider.winfo_width()
        if slider_width > 1:
            knob_offset = 12
            x = knob_offset + (value / 100) * (slider_width - knob_offset * 2) 
            self.bear_icon.place(in_=self.slider, x=x, rely=0.5, anchor="center")
        self.after(50, lambda: self._on_slide(self.slider.get()))
            
    def hide_bear(self):
        self.bear_icon.place_forget()
        
    def _start_drag(self, _event):
        self.is_dragging = True
        
    def _stop_drag(self, _event):
        self.is_dragging = False
        
        