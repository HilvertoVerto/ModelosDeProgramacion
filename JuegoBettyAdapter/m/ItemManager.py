"""Gestor de ítems en el suelo"""
import pygame
import time
import random
from m.Constants import *


class ItemManager:
    """Gestiona spawn, física y colisión de ítems"""
    
    def __init__(self):
        self.items = []
        self.last_spawn = time.time()
        self.spawn_interval = ITEM_SPAWN_INTERVAL

    def spawn_random_item(self):
        """Genera un ítem aleatorio que cae desde arriba"""
        x = random.randint(50, SCREEN_W - 100)
        item_type = random.choice(["clothes", "forehead", "speed"])
        
        self.items.append({
            "x": x, "y": 0, 
            "type": item_type, 
            "param": item_type,
            "vy": ITEM_FALL_SPEED,
            "falling": True
        })

    def update(self, dt):
        """Actualiza física de caída de ítems"""
        ground_level = GROUND_Y - ICON_SIZE
        
        for item in self.items:
            if item.get("falling", True):
                item["y"] += item.get("vy", ITEM_FALL_SPEED) * dt
                if item["y"] >= ground_level:
                    item["y"] = ground_level
                    item["falling"] = False
                    item["vy"] = 0
        
        # Spawn automático
        now = time.time()
        if now - self.last_spawn >= self.spawn_interval:
            self.spawn_random_item()
            self.last_spawn = now

    def check_collision(self, player_rect, buff_manager, buff_duration):
        """Verifica colisiones y aplica buffs"""
        for item in self.items[:]:
            item_rect = pygame.Rect(item["x"], item["y"], ICON_SIZE, ICON_SIZE)
            if player_rect.colliderect(item_rect):
                buff_manager.apply_buff(item["type"], item["param"], buff_duration)
                self.items.remove(item)

    def get_items(self):
        """Retorna lista de ítems para renderizado"""
        return self.items