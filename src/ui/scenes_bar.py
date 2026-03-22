import customtkinter as ctk

class ScenesBar(ctk.CTkFrame):
    
    def __init__(self, master, movie, relax, bright):
        super().__init__(master)
        
        self.pack(fill="x", padx=20, pady=10)
        
        movie_btn = ctk.CTkButton(
            self,
            text="Movie",
            command=movie
        )
        movie_btn.pack(side="left", expand=True, padx=5)
        
        relax_btn = ctk.CTkButton(
            self,
            text="Relax",
            command=relax
        )
        relax_btn.pack(side="left", expand=True, padx=5)
        
        bright_btn = ctk.CTkButton(
            self,
            text="Bright",
            command=bright
        )
        bright_btn.pack(side="left", expand=True, padx=5)