import customtkinter as ctk

class SceneCard(ctk.CTkFrame):
    
    def __init__(
        self,
        master,
        scene: dict,
        palette: list[str],
        command
    ):
        super().__init__(
            master,
            fg_color="#151A17",
            corner_radius=20,
            border_width=1,
            border_color="#2B3138",
        )
        
        self.scene = scene
        self.palette = palette
        
        self.button = ctk.CTkButton(
            self,
            text=scene["name"],
            fg_color="transparent",
            hover_color="#1D2E25",
            text_color="#D2EDE0",
            font=("Segoe UI", 15, "bold"),
            corner_radius=16,
            command=command,
        )
        self.button.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(8, 4)
        )
        
        self.palette_bar = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=8,
        )
        self.palette_bar.pack(
            fill="x",
            padx=10,
            pady=(0,8),
        )
        
        if palette:
            for color in palette[:4]:
                stripe = ctk.CTkFrame(
                    self.palette_bar,
                    fg_color=color,
                    width=20,
                    height=6,
                    corner_radius=3,
                )
                stripe.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=1,
                )
                
    def set_active(
        self,
        active: bool,
        scene_color: str,
    ):
        
        if active:
            self.configure(
                
            )
        