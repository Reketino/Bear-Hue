import customtkinter as ctk

class ControlsBar(ctk.CTkFrame):
    
    def __init__(self, master, on_all, off_all, toggle_bear_mode):
        super().__init__(master, fg_color="transparent")
        
        container = ctk.CTkFrame(self, fg_color="#232323", corner_radius=15)
        container.pack(fill="x", padx=15, pady=10)
        
        self.bear_banner = ctk.CTkLabel(
            container,
            text="🐻Bear Mode",
            font=("Segoe UI", 18, "bold"),
            text_color="#A3B18A"
        )
        self.bear_banner.grid(row=0, column=0, columnspan=2, pady=(5, 5))
        self.bear_banner.grid_remove()
        
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=0)
        
        left = ctk.CTkFrame(container, fg_color="#1A1A1A")
        left.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        on_button = ctk.CTkButton(
            left,
            text="All Lights ON",
            command=on_all,
            fg_color="#81B29A", 
            hover_color="#388E3C",
            text_color="white",
            corner_radius=12,
            width=90
        )
        on_button.pack(side="left")
        
        off_button = ctk.CTkButton(
            left,
            text="All Lights OFF",
            command=off_all,
            fg_color="#4C191B",
            hover_color="#972D07",
            text_color="white",
            corner_radius=12,
            width=90
        )
        off_button.pack(side="left")
        
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        bear_button = ctk.CTkButton(
            right,
            text="🐻Bear Mode",
            command=toggle_bear_mode,
            fg_color="#33261D", 
            hover_color="#6E4420",
            corner_radius=12,
            width=90
        )
        bear_button.pack()
        self.bear_banner.lift() 