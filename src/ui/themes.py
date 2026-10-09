from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    background: str
    panel: str
    card: str
    card_hover: str
    border: str
    border_active: str
    
    text: str
    text_muted: str
    
    accent: str
    accent_hover: str
    
    success: str
    danger: str
    
    slider_background: str
    slider_progress: str
    slider_button: str
    slider_button_hover: str
    