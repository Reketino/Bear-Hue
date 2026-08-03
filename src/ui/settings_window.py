import customtkinter as ctk

from src.settings.settings_manager import SettingsManager


class SettingsWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        settings: SettingsManager,
    ) -> None:
        super().__init__(master)