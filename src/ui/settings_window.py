import customtkinter as ctk

from src.settings.settings_manager import SettingsManager


class SettingsWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        settings: SettingsManager,
    ) -> None:
        super().__init__(master)
        
        self.settings = settings
        
        self.title("Settings")
        self.geometry("360x420")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Segoe UI", 22, "bold"),
        )
        self.label.pack(pady=(20, 25))
        
        self.remember_bear_mode = ctk.CTkCheckBox(
            self,
            text="Remember Bear Mode",
            command=self.toggle_remember_bear_mode,
        )
        self.remember_bear_mode.pack(
            anchor="w",
            padx=30,
            pady=10,
        )
        
        
    def toggle_remember_bear_mode(self) -> None:
        self.settings.set(
            "remember_bear_mode",
            bool(self.remember_bear_mode.get()),
        )