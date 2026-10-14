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
    
    glow: str
    

DARK_THEME = Theme(
    background="#101010",
    panel="#101312",
    card="#151A17",
    card_hover="#1D2E25",
    border="#2B3138",
    border_active="#6BAF92",
    
    text="#D2EDE0",
    text_muted="#9BA9A3",
    
)
    