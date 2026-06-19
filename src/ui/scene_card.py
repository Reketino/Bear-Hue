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