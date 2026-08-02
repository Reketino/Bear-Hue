import json
from pathlib import Path
from typing import Any

from src.settings.defaults import DEFAULT_SETTINGS

SETTINGS_FILE = Path("settings.json")

class SettingsManager:
    def __init__(self) -> None:
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()
    
        
    def load(self) -> None:
        if not SETTINGS_FILE.exists():
            self.save()
            return
        
        try: 
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            self.settings.update(data)
            
        except (OSError, json.JSONDecodeError):
            self.settings = DEFAULT_SETTINGS.copy()
            self.save()
    
            
    def save(self) -> None:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.settings,
                file,
                indent=4,
                ensure_ascii=False,
            )
            
    def get(self, key: str):
        return self.settings.get(key)
    
    def set(self, key: str, value):
        self.settings[key] = value
        self.save()