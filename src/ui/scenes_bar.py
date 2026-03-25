import customtkinter as ctk

class ScenesBar(ctk.CTkFrame):
    
    def __init__(self, master, hue_service):
        super().__init__(master)
        self.pack(fill="x", padx=20, pady=10)
        scenes = hue_service.get_scenes()
        columns = 2
        for i, scene in enumerate(scenes):
            color = hue_service.get_scene_color(scene["id"])
            row = i // columns
            col = i % columns
            btn = ctk.CTkButton(
                self,
                text=scene["name"],
                height=70,
                corner_radius=15,
                fg_color=color,
                hover_color=self._darken(color),
                command=lambda s=scene["id"]: hue_service.activate_scene(s)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            for col in range(columns):
                self.grid_columnconfigure(col, weight=1)
                
        
    def _darken(self, hex_color, factor =0.8):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:3], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[3:4], 16)
        return  "#{:02x}{:02x}{:02x}".format(
            int(r * factor),
            int(g * factor),
            int(b * factor)
        )
        
    def _is_light(self, hex_color):
        hex_color = hex_color.lstrips("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.1114 * b)
        return luminance > 140
        