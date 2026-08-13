import customtkinter as ctk

from src.services.hue_service import HueService
from src.settings.settings_manager import SettingsManager
from src.ui.scene_card import SceneCard

class ScenesBar(ctk.CTkFrame):
    
    def __init__(
        self, 
        master, 
        hue_service: HueService,
        settings: SettingsManager,
        ) -> None:
        super().__init__(
            master,
            fg_color="#101312",
            corner_radius=20
            )
        
        self.hue_service = hue_service
        self.settings = settings
        self.active_scene = None
        self.buttons = {}
        self.scene_colors = {}
        
        self.pack(
            fill="x", 
            padx=15, 
            pady=10
        )
       
        scenes = hue_service.get_scenes()
        columns = 2
        
        for col in range(columns):
            self.grid_columnconfigure(col, weight=1)       
            
        show_scene_colors = self.settings.get(
            "show_scene_colors"
        ) 
        
        for i, scene in enumerate(scenes):
            scene_id = scene["id"]
            
            color = hue_service.get_scene_color(scene_id)
            
            palette = hue_service.get_scene_palette(scene["name"])
            
            row = i // columns
            col = i % columns
            
            card = SceneCard(
                self,
                scene=scene,
                palette=palette,
                command=lambda s=scene["id"]: self._on_scene_click(s)
            )
            card.grid(
                row=row, 
                column=col, 
                padx=6, 
                pady=6, 
                sticky="ew"
            )
            
            card.set_palette_visible(
                show_scene_colors
            )
            self.scene_colors[scene["id"]] = color
            self.buttons[scene["id"]] = card
            
        if scenes and len(self.buttons) > 0:
            self.set_active(scenes[0]["id"])
            
            
    def _on_scene_click(
        self, 
        scene_id: str,
        ) -> None:
        self.hue_service.activate_scene(
            scene_id
        )
        self.set_active(scene_id)
       
        
    def set_active(self, scene_id):
        self.active_scene = scene_id
        
        for sid, card in self.buttons.items():
            card.set_active(
                sid == scene_id,
                self.scene_colors[sid]
            ) 
            
    def set_bear_mode(
        self,
        enabled: bool
    ):
        for card in self.buttons.values():
            card.set_bear_mode(enabled)
        

        