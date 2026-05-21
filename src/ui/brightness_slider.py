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
            height=28
        )
        self.slider.pack(fill="x", padx=30, pady=20)
        self.slider.bind("<ButtonPress-1>", self._start_drag)
        self.slider.bind("<ButtonRelease-1>", self._stop_drag)
        
        
    def _on_slide(self, value):
        if self.external_command:
            self.external_command(value)
                   

    def _start_drag(self, _):
        self.is_dragging = True
        
    def _stop_drag(self, _):
        self.is_dragging = False
        
        