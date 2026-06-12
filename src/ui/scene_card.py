import customtkinter as ctk

class SceneCard(ctk.CTkFrame):
    
    def __init__(
        self,
        master,
        scene: dict,
        palette: list[str],
        command
    ):