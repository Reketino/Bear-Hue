import customtkinter as ctk

class ControlsBar(ctk.CTkFrame):
    
    def __init__(self, master, on_all, off_all, toggle_bear_mode):
        super().__init__(master, fg_color="transparent")
        
        container = ctk.CTkFrame(self, fg_color="#232323", corner_radius=15)
        container.pack(fill="x", padx=15, pady=10)
        
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        on_button = ctk.CTkButton(
            left,
            text="All Lights ON",
            command=on_all,
            fg_color="#2A2A2A",
            hover_color="#3A3A3A",
            text_color="white",
            corner_radius=12
        )
        on_button.pack(side="left")
        
        off_button = ctk.CTkButton(
            left,
            text="All Lights OFF",
            command=off_all,
            fg_color="#3A2A2A",
            hover_color="#4A2F2F",
            text_color="white",
            corner_radius=12
        )
        off_button.pack(side="left")
        
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        bear_button = ctk.CTkButton(
            right,
            text="🐻Bear Mode",
            command=toggle_bear_mode,
            fg_color="#8B5A2B",
            hover_color="#6E4420",
            corner_radius=12
        )
        bear_button.pack() 