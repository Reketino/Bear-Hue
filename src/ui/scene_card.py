import customtkinter as ctk

class SceneCard(ctk.CTkFrame):
    
    def __init__(
        self,
        master,
        scene: dict,
        palette: list[str],
        command
    ):
        super().__init__(
            master,
            fg_color="#151A17",
            corner_radius=20,
            border_width=1,
            border_color="#2B3138",
        )
        
        self.scene = scene
        self.palette = palette
        
        self.button = ctk.CTkButton(
            self,
            text=scene["name"],
            fg_color="transparent",
            hover_color="#1D2E25",
            text_color="#D2EDE0",
            font=("Segoe UI", 15, "bold"),
            corner_radius=16,
            command=command,
        )
        self.button.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(8, 4)
        )
        
        self.palette_bar = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=8,
        )
        self.palette_bar.pack(
            fill="x",
            padx=10,
            pady=(0,8),
        )
        
        self.palette_stripes = []
        
       
        for color in palette[:4]:
            stripe = ctk.CTkFrame(
                self.palette_bar,
                fg_color=color,
                width=20,
                height=6,
                corner_radius=3,
            )
            stripe.pack(
                side="left",
                fill="x",
                expand=True,
                padx=1,
            )
            
            self.palette_stripes.append(stripe)
            
    def set_palette_visible(self, visible: bool) -> None:
        if visible:
            self.palette_bar.pack(
                fill="x",
                padx=10,
                pady=(0, 8),
            )
        else:
            self.palette_bar.pack_forget()
                
    def set_active(
        self,
        active: bool,
        scene_color: str,
    ) -> None:
        if active:
            self.configure(
                fg_color=self._darken(scene_color, 0.12),
                border_width=3,
                border_color=scene_color,   
            )
            
        else: 
            self.configure(
                fg_color="#151A17",
                border_width=1,
                border_color=self._darken(
                    scene_color,
                    0.75,
                ),
            )
            
    def set_bear_mode(
        self,
        enabled: bool,  
    ):
        if enabled:
            self.configure(
                fg_color="#18201B",
                border_color="#6BAF92",
            )
        else: 
            self.configure(
                fg_color="#151A17",
                border_color="#2B3138",
            )
            self.button.configure(
                hover_color="#1D2E25",
            )
            
            
    def _darken(self, hex_color, factor =0.8):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return "#333333"
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
        except ValueError:
            return "#333333"
        
        r = max(int(r * factor), 0)
        g = max(int(g * factor), 0)
        b = max(int(b * factor), 0)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)   
        