import customtkinter as ctk

class ScenesBar(ctk.CTkFrame):
    
    def __init__(self, master, hue_service):
        super().__init__(master)
        self.pack(fill="x", padx=20, pady=10)
        scenes = hue_service.get_scenes()
        columns = 2
        for i, scene in enumerate(scenes):
            row = i // columns
            col = i % columns
            btn = ctk.CTkButton(
                self,
                text=scene["name"],
                command=lambda s=scene["id"]: hue_service.activate_scene(s)
            )
            btn.pack(side="left", expand=True, padx=5)
        