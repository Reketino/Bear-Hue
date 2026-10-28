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
    
    accent="#6BAF92",
    accent_hover="#9BA9A3",
    
    success="#6BAF92",
    danger="#6B2020",
    
    slider_background="#4F4F4F",
    slider_progress="#CFE6FD",
    slider_button="#011120",
    slider_button_hover="#A3BECC",
    
    glow="#1A221D",
)

LIGHT_THEME = Theme(
    background="#F2F2F2",
    panel="#E7E7E7",
    card="#FFFFFF",
    card_hover="#E8F2EC",
    border="#D0D5D2",
    border_active="#4F8F70",
    
    text="#17211C",
    text_muted="#667168",
    
    accent="#4F8F70",
    accent_hover="#67A585",
    
    success="#4F8F70",
    danger="#A33A3A",
    
    slider_background= "#C7CBC9",
    slider_progress="#A9D0BC",
    slider_button="#183326",
    slider_button_hover="#315C46",
    
    glow="#DCEBE2",
)

BEAR_DARK_THEME = Theme(
    background="#0B0F0D",
    panel="#101612",
    card="#18201B",
    card_hover="#203529",
    border="#355443",
    border_active="#6BAF92",
    
    text="#D2EDE0",
    text_muted="#9BB2A5",
    
    accent="#6BAF92",
    accent_hover="#86C8A6",
    
)


    