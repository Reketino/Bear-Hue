import customtkinter as ctk

class ControlsBar(ctk.CTkFrame):
    
    def __init__(self, master, on_all, off_all):
        super().__init__(master)
        
        self.pack(fill="x", padx=20, pady=20)
        
        on_button = ctk.CTkButton(
            self,
            text="All Lights ON",
            command=on_all
        )
        on_button.pack(side="left", padx=10)
        
        off_button = ctk.CTkButton(
            self,
            text="All Lights OFF",
            command=off_all
        )
        off_button.pack(side="right", padx=10)