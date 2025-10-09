"""Vista del juego - Renderización gráfica"""
import pygame
import os
from m.Constants import SCREEN_W, SCREEN_H, GROUND_Y, ICON_SIZE, BORDER_WIDTH
from v.UIRenderer import UIRenderer


class Vista:
    """Gestiona la renderización del juego - Patrón MVC"""
    
    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Don Armando - Buffs Activos")
        
        self.background = self._load_background()
        self.buff_icons = self._load_icons()
        self.font = pygame.font.SysFont("Arial", 20)
        self.ui_renderer = UIRenderer(self.screen, self.buff_icons, self.font)

    def _load_background(self):
        """Carga imagen de fondo"""
        try:
            bg = pygame.image.load(os.path.join("graficos", "Fondo", "Fondo.png")).convert()
            return pygame.transform.scale(bg, (SCREEN_W, SCREEN_H))
        except:
            return None

    def _load_icons(self):
        """Carga íconos de buffs"""
        icons = {}
        icon_files = {"forehead": "Buff_Frente.png", "vestido": "Buff_Ropa.png", 
                     "caballeria": "Buff_Ropa.png", "speed": "Buff_Correr.png"}
        
        for key, fname in icon_files.items():
            try:
                icons[key] = pygame.image.load(os.path.join("graficos", "Bufos", fname)).convert_alpha()
            except:
                surf = pygame.Surface((32, 32))
                color = (0, 200, 255) if key == "forehead" else (255, 0, 255) if key in ["vestido", "caballeria"] else (255, 255, 0)
                surf.fill(color)
                icons[key] = surf
        return icons

    def draw(self, dt, input_mode=None):
        """Dibuja todos los elementos"""
        # Fondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((30, 30, 40))
        
        # Suelo
        pygame.draw.rect(self.screen, (100, 180, 100), (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
        
        # Ítems
        self._draw_items()
        
        # Jugador
        sprite = self.model.player.get_sprite(dt)
        self.screen.blit(sprite, (int(self.model.player.x), int(self.model.player.y)))
        
        # UI
        self.ui_renderer.draw_buffs(self.model.buff_manager)
        self.ui_renderer.draw_debug_info(self.model.player, GROUND_Y, SCREEN_H, input_mode)
        
        pygame.display.flip()

    def _draw_items(self):
        """Dibuja ítems en el suelo con esquinas redondeadas"""
        border_radius = 8  # Radio de esquinas redondeadas
        
        for item in self.model.items_on_floor:
            x, y = int(item["x"]), int(item["y"])
            
            # Fondo blanco con esquinas redondeadas
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
            
            # Ícono
            icon_key = "vestido" if item["type"] == "clothes" else item["type"]
            icon = self.buff_icons.get(icon_key)
            if icon:
                # Escalar ícono
                icon_scaled = pygame.transform.scale(icon, (ICON_SIZE, ICON_SIZE))
                
                # Crear superficie con transparencia para recortar esquinas
                icon_surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
                
                # Dibujar máscara de esquinas redondeadas
                pygame.draw.rect(icon_surface, (255, 255, 255, 255), (0, 0, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
                
                # Aplicar ícono con máscara
                icon_surface.blit(icon_scaled, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                self.screen.blit(icon_surface, (x, y))
            else:
                # Colores de respaldo con esquinas redondeadas
                colors = {"clothes": (255, 0, 255), "forehead": (0, 200, 255), "speed": (255, 255, 0)}
                pygame.draw.rect(self.screen, colors.get(item["type"], (255, 255, 255)), 
                               (x, y, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
            
            # Borde negro con esquinas redondeadas
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, ICON_SIZE, ICON_SIZE), BORDER_WIDTH, border_radius=border_radius)