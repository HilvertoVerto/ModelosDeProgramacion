"""
Modelo principal - Coordina todos los componentes

PATRÓN DECORATOR EN ACCIÓN:
El BuffManager gestiona los decoradores que modifican al jugador.
"""
import pygame
from m.Constants import *
from m.SpriteLoader import SpriteLoader
from m.Player import BasePlayer
from m.BuffManager import BuffManager
from m.ItemManager import ItemManager


class Modelo:
    """Modelo principal del juego - Patrón MVC"""
    
    def __init__(self, sprite_root="graficos/Sprites"):
        self.sprite_loader = SpriteLoader(sprite_root)
        
        # COMPONENTE BASE (sin decorar)
        self.player = BasePlayer(sprite_loader=self.sprite_loader)
        
        # GESTOR DE DECORADORES
        self.buff_manager = BuffManager()
        
        self.item_manager = ItemManager()
        self.buff_duration = BUFF_DURATION
        self.active_buffs = []
        
        # Para compatibilidad con Vista
        self.items_on_floor = self.item_manager.items

    def update(self, dt):
        """
        Actualiza el estado del juego.
        
        PATRÓN DECORATOR EN ACCIÓN:
        El BuffManager mantiene los decoradores y los aplica al jugador.
        """
        # Actualizar ítems
        self.item_manager.update(dt)
        
        # Actualizar decoradores (pueden expirar)
        self.buff_manager.update()
        
        # ===== APLICAR DECORADORES AL JUGADOR =====
        # Obtener el jugador decorado
        decorated = self.buff_manager.get_decorated_player()
        appearance = decorated.get_appearance()
        
        # DECORADOR: Apariencia de ropa
        self.player.base_category = appearance["clothes"]
        
        # DECORADOR: Tamaño de frente
        self.player.front_index = appearance["forehead"]
        
        # DECORADOR: Velocidad aumentada
        self.player.base_speed = decorated.get_speed()
        
        # El jugador funciona normalmente con sus propiedades decoradas
        self.player.update_physics(dt)
        
        # Verificar colisiones con ítems
        player_rect = self.get_player_rect()
        self.item_manager.check_collision(player_rect, self.buff_manager, self.buff_duration)

    def get_player_rect(self):
        """Retorna rectángulo de colisión del jugador"""
        return pygame.Rect(
            int(self.player.x), int(self.player.y), 
            self.player.sprite_width, self.player.sprite_height
        )