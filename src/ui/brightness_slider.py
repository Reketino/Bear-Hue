import customtkinter as ctk

class BrightnessSlider(ctk.CTkFrame):
    
    def __init__(self, master, command):
        super().__init__(master)
        
        self.external_command = command
        self.is_dragging = False
         
        self.label = ctk.CTkLabel(self, text="Brightness")
        self.label.pack(pady=(10, 0))
        
        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self._on_slide,
            button_length= 1,
            height=20
        )
        self.slider.pack(fill="x", padx=30, pady=20)
        self.slider.bind("<ButtonPress-1>", self._start_drag)
        self.slider.bind("<ButtonRelease-1>", self._stop_drag)
        
        self.bear_icon = ctk.CTkLabel(
            self,
            text="🐻",
            font=("Segoe UI Emoji", 22)
        )
        self.after(100, self.update_bear_position)
        
    def _on_slide(self, value):
        self.update_bear_position()
        if self.external_command:
            self.external_command(value)
                   
    def update_bear_position(self):
        self.update_idletasks()
        val = self.slider.get()
        width = self.slider.winfo_width()
        if width <= 1:
            return
        knob_size = 10
        track_padding = 0
        usable = width - (track_padding * 2)
        x = track_padding + (val / 100) * usable
        x = x - knob_size / 2
        self.bear_icon.place(
            in_=self.slider,
            x=x,
            rely=0.5,
            anchor="center"
        )
          
    def show_bear(self):
        self.update_bear_position()
        self.bear_icon.lift()
            
    def hide_bear(self):
        self.bear_icon.place_forget()
        
    def _start_drag(self, _):
        self.is_dragging = True
        
    def _stop_drag(self, _):
        self.is_dragging = False
        
        