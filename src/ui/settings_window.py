import customtkinter as ctk

from src.settings.settings_manager import SettingsManager

REFRESH_INTERVAL_OPTIONS = [
    500,
    1000,
    2000,
    5000,
]

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
        
        if self.settings.get("remember_bear_mode"):
            self.remember_bear_mode.select()
        else:
            self.remember_bear_mode.deselect()
            
        self.refresh_label = ctk.CTkLabel(
            self,
            text="Refresh interval",
            font=("Segoe UI", 14),
        )
        self.refresh_label.pack(
            anchor="w",
            padx=30,
            pady=(20, 5),
        )
        
        self.refresh_interval = ctk.CTkOptionMenu(
            self,
            values=[
                f"{value} ms"
                for value in REFRESH_INTERVAL_OPTIONS
            ],
            command=self.change_refresh_interval,
            width=140,
        )
        self.refresh_interval.pack(
            anchorr="w",
            padx=30,
            pady=5,
        )
        
        current_interval = self.settings.get(
            "refresh_interval"
        )
        
        
    def toggle_remember_bear_mode(self) -> None:
        self.settings.set(
            "remember_bear_mode",
            bool(self.remember_bear_mode.get()),
        )