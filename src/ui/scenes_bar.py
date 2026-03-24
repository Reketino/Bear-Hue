import customtkinter as ctk

class ScenesBar(ctk.CTkFrame):
    
    def __init__(self, master, hue_service):
        super().__init__(master)
        
        self.pack(fill="x", padx=20, pady=10)
        
        