import customtkinter as ctk

from src.services.hue_service import HueService
from src.settings.settings_manager import SettingsManager
from src.ui.scenes_bar import ScenesBar

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
        scenes: ScenesBar,
    ) -> None:
        super().__init__(master)
        
        self.settings = settings
        self.scenes = scenes
        
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
            anchor="w",
            padx=30,
            pady=5,
        )
        
        current_interval = self.settings.get(
            "refresh_interval"
        )
        
        self.refresh_interval.set(
            f"{current_interval} ms"
        )
        
        self.show_scene_colors = ctk.CTkCheckBox(
            self,
            text="Show Scene Colors",
            command=self.toggle_show_scene_colors
        )
        self.show_scene_colors.pack(
            anchor="w",
            padx=30,
            pady=10,
        )
        
        if self.settings.get("show_scene_colors"):
            self.show_scene_colors.select()
        else:
            self.show_scene_colors.deselect()
             
    def toggle_remember_bear_mode(self) -> None:
        self.settings.set(
            "remember_bear_mode",
            bool(self.remember_bear_mode.get()),
        )
        
    def change_refresh_interval(self, value: str) -> None:
        interval = int(
            value.replace(" ms", "")
        )
        
        self.settings.set(
            "refresh_interval",
            interval,
        )
    
    def toggle_show_scene_colors(self) -> None:
        enabled = bool(
            self.show_scene_colors.get()
        )
            
        self.scenes.set_show_scene_colors(
            enabled
        )
        
        