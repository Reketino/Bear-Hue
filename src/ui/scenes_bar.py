import customtkinter as ctk

class ScenesBar(ctk.CTkFrame):
    
    def __init__(self, master, hue_service):
        super().__init__(master)
        
        self.hue_service = hue_service
        self.active_scene = None
        self.buttons = {}
        self.pack(fill="x", padx=20, pady=10)
       
        scenes = hue_service.get_scenes()
        columns = 2
        
        for col in range(columns):
            self.grid_columnconfigure(col, weight=1)        
        for i, scene in enumerate(scenes):
            color = hue_service.get_scene_color(scene["id"])
            
            row = i // columns
            col = i % columns
            
            btn = ctk.CTkButton(
                self,
                text=scene["name"],
                height=70,
                fg_color=color,
                hover_color=self._darken(color),
                text_color="black" if self._is_light(color) else "white",
                corner_radius=15,
                border_width=2,
                border_color=self._darken(color, 0.6),
                command=lambda s=scene["id"]: self._on_scene_click(s)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.buttons[scene["id"]] = btn
        if scenes and len(self.buttons) > 0:
            self.set_active(scenes[0]["id"])
            
            
    def _on_scene_click(self, scene_id):
        self.hue_service.activate_scene(scene_id)
        self.set_active(scene_id)
       
        
    def set_active(self, scene_id):
        self.active_scene = scene_id
        for sid, btn in self.buttons.items():
            if sid == scene_id:
                btn.configure(
                    border_width=4,
                    border_color=self._lighten(btn.cget("fg_color"), 1.4)
                )
            else:
                btn.configure(
                    border_width=2,
                    border_color=self._darken(btn.cget("fg_color"), 0.6)
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
        return "#{:02}{:02}{:02}".format(r, g, b)   
        
        
        
    def _lighten(self, hex_color, factor=1.3):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return "#AAAAAA"
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
        except ValueError:
            return "#AAAAAA"
        r = min(int(r * factor), 255)
        g = min(int(g * factor), 255)
        b = min(int(b * factor), 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    
        
    def _is_light(self, hex_color):
        if not hex_color or len(hex_color) < 7:
            return False
        hex_color = hex_color.lstrip("#")
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
        except ValueError:
            return False
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        return luminance > 140
        