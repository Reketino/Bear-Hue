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