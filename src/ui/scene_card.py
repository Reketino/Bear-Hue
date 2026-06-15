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