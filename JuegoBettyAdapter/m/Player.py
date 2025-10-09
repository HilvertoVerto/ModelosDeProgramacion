"""Clase del jugador (Don Armando)"""
import pygame
from m.Constants import *


class BasePlayer:
    """Representa a Don Armando con física, movimiento y animaciones"""
    
    def __init__(self, x=100, y=GROUND_Y - 64, sprite_loader=None):
        self.sprite_loader = sprite_loader
        self.x, self.y = x, GROUND_Y - 80
        self.vx, self.vy = 0, 0
        self.sprite_width, self.sprite_height = 60, 80
        self.on_ground, self.moving = True, False
        self.facing = "right"
        self.base_category, self.front_index = "traje", 0
        self.anim_timer, self.anim_frame = 0.0, 0
        self.base_speed = BASE_SPEED
        self.first_sprite_loaded = False

    def update_physics(self, dt):
        """Actualiza física del jugador"""
        # Gravedad
        if not self.on_ground:
            self.vy += GRAVITY * dt
        self.y += self.vy * dt
        
        # Límites verticales
        ground_limit = GROUND_Y - self.sprite_height
        if self.y >= ground_limit:
            self.y, self.vy, self.on_ground = ground_limit, 0, True
        else:
            self.on_ground = False
        
        ceiling_limit = GROUND_Y - self.sprite_height - 200
        if self.y < ceiling_limit:
            self.y = ceiling_limit
            self.vy = max(0, self.vy)
        
        # Movimiento horizontal
        self.x += self.vx * dt
        self.x = max(0, min(SCREEN_W - self.sprite_width, self.x))

    def jump(self):
        """Salta si está en el suelo"""
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def get_speed(self):
        return self.base_speed

    def get_sprite(self, dt):
        """Obtiene sprite actual con animación"""
        self.anim_timer += dt
        if self.moving:
            if self.anim_timer > 0.15:
                self.anim_frame = (self.anim_frame + 1) % 2
                self.anim_timer = 0.0
            action = "mov" if self.anim_frame == 0 else "quieto"
        else:
            action, self.anim_frame = "quieto", 0
            
        surf = self.sprite_loader.get(self.base_category, self.front_index, action, 0)
        
        # Primera carga: ajustar dimensiones
        if not self.first_sprite_loaded:
            self.sprite_width = surf.get_width()
            self.sprite_height = surf.get_height()
            self.y = GROUND_Y - self.sprite_height
            self.first_sprite_loaded = True
        
        return pygame.transform.flip(surf, True, False) if self.facing == "left" else surf