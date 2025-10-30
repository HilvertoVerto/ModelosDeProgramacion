import pygame
import time
import os
import random
from typing import List, Dict, Any

SCREEN_W, SCREEN_H = 800, 600
GROUND_Y = 520  # Más cerca del borde inferior
GRAVITY = 1200
JUMP_VELOCITY = -520
BASE_SPEED = 250  # Aumentamos la velocidad base para que se note más

def load_image(path, scale=1.0):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

class SpriteLoader:
    def __init__(self, sprites_root="graficos/Sprites"):
        self.root = sprites_root
        self.cache = {}

    def get(self, categoria, frente_index, action, frame_idx):
        key = (categoria, frente_index, action, frame_idx)
        if key in self.cache:
            return self.cache[key]

        folder = f"frente{frente_index}"
        base_names = {
            "traje": ("traje_mov_f{f}.png", "traje_quieto_f{f}.png"),
            "vestido": ("vestido_mov_f{f}.png", "vestido_quieto_f{f}.png"),
            "caballeria": ("cab_mov_f{f}.png", "cab_quieto_f{f}.png")
        }
        mov_name, quiet_name = base_names[categoria]
        fname = mov_name.format(f=frente_index) if action == "mov" else quiet_name.format(f=frente_index)
        path = os.path.join(self.root, categoria, folder, fname)
        surf = load_image(path, scale=0.6)  # Reducimos más el scale
        self.cache[key] = surf
        return surf

class BasePlayer:
    def __init__(self, x=100, y=GROUND_Y - 64, sprite_loader=None):
        self.sprite_loader = sprite_loader
        self.x = x
        self.base_category = "traje"
        self.front_index = 0
        self.anim_timer = 0.0
        self.anim_frame = 0
        self.facing = "right"
        
        # Dimensiones iniciales estimadas (se actualizarán al cargar el sprite)
        self.sprite_width = 60
        self.sprite_height = 80
        
        # Posición Y: los pies deben estar sobre el suelo
        self.y = GROUND_Y - self.sprite_height
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.moving = False
        self.base_speed = BASE_SPEED
        self.first_sprite_loaded = False

    def update_physics(self, dt):
        # Aplicar gravedad
        if not self.on_ground:
            self.vy += GRAVITY * dt
        
        # Actualizar posición Y
        self.y += self.vy * dt
        
        # LÍMITE INFERIOR: No puede bajar del suelo
        ground_limit = GROUND_Y - self.sprite_height
        if self.y >= ground_limit:
            self.y = ground_limit
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # LÍMITE SUPERIOR: No puede subir demasiado
        ceiling_limit = GROUND_Y - self.sprite_height - 200
        if self.y < ceiling_limit:
            self.y = ceiling_limit
            self.vy = max(0, self.vy)  # Solo detenemos si está subiendo
        
        # Actualizar posición X
        self.x += self.vx * dt
        
        # LÍMITES HORIZONTALES
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_W - self.sprite_width:
            self.x = SCREEN_W - self.sprite_width

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def get_speed(self):
        return self.base_speed

    def get_category(self):
        return self.base_category

    def get_front(self):
        return self.front_index

    def get_sprite(self, dt):
        self.anim_timer += dt
        if self.moving:
            # Alternar entre imagen de movimiento (frame 0) y quieto (frame 1) 
            # para dar ilusión de caminar
            if self.anim_timer > 0.15:  # Cada 0.15 segundos cambia
                self.anim_frame = (self.anim_frame + 1) % 2
                self.anim_timer = 0.0
            
            # Frame 0 = mov, Frame 1 = quieto (alternando)
            action = "mov" if self.anim_frame == 0 else "quieto"
        else:
            action = "quieto"
            self.anim_frame = 0
            
        surf = self.sprite_loader.get(self.base_category, self.front_index, action, 0)
        
        # Actualizar dimensiones reales del sprite la primera vez
        if not self.first_sprite_loaded:
            old_height = self.sprite_height
            self.sprite_width = surf.get_width()
            self.sprite_height = surf.get_height()
            # Ajustar posición Y según nueva altura
            self.y = GROUND_Y - self.sprite_height
            self.first_sprite_loaded = True
        
        if self.facing == "left":
            surf = pygame.transform.flip(surf, True, False)
        return surf

class BuffManager:
    def __init__(self):
        self.front_level = 0
        self.front_expire = 0
        self.clothes_type = "traje"
        self.clothes_expire = 0
        self.speed_level = 0  # Nivel de velocidad acumulable
        self.speed_expire = 0
        self.max_speed_level = 3  # Máximo 3 niveles de velocidad

    def get_speed_multiplier(self):
        """Retorna el multiplicador de velocidad según el nivel"""
        if self.speed_level == 0:
            return 1.0
        elif self.speed_level == 1:
            return 1.5  # 50% más rápido
        elif self.speed_level == 2:
            return 2.0  # 100% más rápido
        else:  # nivel 3
            return 2.5  # 150% más rápido

    def apply_buff(self, buff_type, param, duration):
        now = time.time()
        if buff_type == "forehead":
            if self.front_level < 3:
                self.front_level += 1
            self.front_expire = now + duration
        elif buff_type == "clothes":
            # Jerarquía: traje (0) -> vestido (1) -> caballeria (2)
            order = {"traje": 0, "vestido": 1, "caballeria": 2}
            current_level = order[self.clothes_type]
            
            # Si agarra un poder de ropa, sube al siguiente nivel en la jerarquía
            if self.clothes_type == "traje":
                # Si está en traje, el siguiente es vestido
                self.clothes_type = "vestido"
                self.clothes_expire = now + duration
            elif self.clothes_type == "vestido":
                # Si está en vestido, el siguiente es caballeria
                self.clothes_type = "caballeria"
                self.clothes_expire = now + duration
            elif self.clothes_type == "caballeria":
                # Si ya está en caballeria (máximo), solo reinicia el tiempo
                self.clothes_expire = now + duration
                
        elif buff_type == "speed":
            # Velocidad acumulable hasta nivel 3
            if self.speed_level < self.max_speed_level:
                self.speed_level += 1
            self.speed_expire = now + duration

    def update(self):
        now = time.time()
        if self.front_expire and now >= self.front_expire:
            self.front_level -= 1
            if self.front_level < 0:
                self.front_level = 0
            if self.front_level > 0:
                self.front_expire = now + 10
            else:
                self.front_expire = 0
        if self.clothes_expire and now >= self.clothes_expire:
            self.clothes_type = "traje"
            self.clothes_expire = 0
        if self.speed_expire and now >= self.speed_expire:
            self.speed_level -= 1
            if self.speed_level < 0:
                self.speed_level = 0
            if self.speed_level > 0:
                self.speed_expire = now + 10
            else:
                self.speed_expire = 0

class Modelo:
    def __init__(self, sprite_root="graficos/Sprites"):
        self.sprite_loader = SpriteLoader(sprite_root)
        self.player = BasePlayer(sprite_loader=self.sprite_loader)
        self.buff_manager = BuffManager()
        self.items_on_floor: List[Dict[str, Any]] = []
        self.last_item_spawn = time.time()
        self.item_spawn_interval = 5.0
        self.buff_duration = 10.0
        self.active_buffs = []

    def spawn_random_item(self):
        x = random.randint(50, SCREEN_W - 100)
        y = GROUND_Y - 40  # Los ítems aparecen justo sobre el suelo
        t = random.choice(["clothes", "forehead", "speed"])
        # Para clothes ya no importa el parámetro, solo sube de nivel
        param = "clothes" if t == "clothes" else t
        self.items_on_floor.append({"x": x, "y": y, "type": t, "param": param})

    def pickup_item_if_collide(self, rect):
        for it in self.items_on_floor[:]:
            item_rect = pygame.Rect(it["x"], it["y"], 40, 40)
            if rect.colliderect(item_rect):
                self.buff_manager.apply_buff(it["type"], it["param"], self.buff_duration)
                self.items_on_floor.remove(it)

    def update(self, dt):
        now = time.time()
        if now - self.last_item_spawn >= self.item_spawn_interval:
            self.spawn_random_item()
            self.last_item_spawn = now
        self.buff_manager.update()
        self.player.base_category = self.buff_manager.clothes_type
        self.player.front_index = self.buff_manager.front_level
        self.player.base_speed = BASE_SPEED * self.buff_manager.get_speed_multiplier()
        self.player.update_physics(dt)

    def get_player_rect(self):
        return pygame.Rect(int(self.player.x), int(self.player.y), 
                          self.player.sprite_width, self.player.sprite_height)