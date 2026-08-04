import customtkinter as ctk

from src.settings.settings_manager import SettingsManager


class SettingsWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        settings: SettingsManager,
    ) -> None:
        super().__init__(master)
        
        self.setting = settings
        
        self.title("Settings")
        self.geometry("360x420")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(
            self,
            text="⚙ Settings"
            font=("Segoe UI", 22 "bold"),
        )