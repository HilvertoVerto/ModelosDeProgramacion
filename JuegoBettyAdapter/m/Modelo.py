"""Modelo principal - Coordina todos los componentes"""
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
        self.player = BasePlayer(sprite_loader=self.sprite_loader)
        self.buff_manager = BuffManager()
        self.item_manager = ItemManager()
        self.buff_duration = BUFF_DURATION
        self.active_buffs = []  # Compatibilidad
        
        # Para compatibilidad con Vista (acceso directo a items_on_floor)
        self.items_on_floor = self.item_manager.items

    def update(self, dt):
        """Actualiza el estado del juego"""
        # Actualizar ítems
        self.item_manager.update(dt)
        
        # Actualizar buffs
        self.buff_manager.update()
        
        # Aplicar buffs al jugador
        self.player.base_category = self.buff_manager.clothes_type
        self.player.front_index = self.buff_manager.front_level
        self.player.base_speed = BASE_SPEED * self.buff_manager.get_speed_multiplier()
        
        # Actualizar física del jugador
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