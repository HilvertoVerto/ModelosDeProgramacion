import pygame
import time
from v.Vista import Vista
from m.Modelo import Modelo

class Controlador:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.model = Modelo()
        self.vista = Vista(self.model)
        self.running = True

    def handle_input(self, events):
        keys = pygame.key.get_pressed()
        player = self.model.player

        # Movimiento horizontal
        speed = player.get_speed()
        if keys[pygame.K_LEFT]:
            player.vx = -speed
            player.moving = True
            player.facing = "left"
        elif keys[pygame.K_RIGHT]:
            player.vx = speed
            player.moving = True
            player.facing = "right"
        else:
            player.vx = 0
            player.moving = False

        # Salto
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                player.jump()

    def update_active_buffs_list(self):
        """Actualiza una lista legible de buffs activos para mostrar en la Vista."""
        buffs = []
        bm = self.model.buff_manager

        if bm.front_level > 0:
            buffs.append(f"frente x{bm.front_level}")
        if bm.clothes_type != "traje":
            buffs.append(bm.clothes_type)
        if bm.speed_level > 0:
            buffs.append(f"velocidad x{bm.speed_level}")

        self.model.active_buffs = buffs

    def run(self):
        """Bucle principal del juego"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.handle_input(events)

            # Actualizar modelo
            self.model.update(dt)

            # Detectar colisiones con ítems
            player_rect = self.model.get_player_rect()
            self.model.pickup_item_if_collide(player_rect)

            # Actualizar lista visible de buffs
            self.update_active_buffs_list()

            # Dibujar todo
            self.vista.draw(dt)

        pygame.quit()