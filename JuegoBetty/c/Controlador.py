import pygame
import time
from v.Vista import Vista
from m.Modelo import Modelo

# --------------------------
# NUEVAS CLASES ADAPTADORAS
# --------------------------
class PlayerInput:
    """Interfaz base para adaptadores de entrada."""
    def get_left(self): return False
    def get_right(self): return False
    def get_jump(self, events): return False


class MouseAdapter(PlayerInput):
    """Adaptador que controla al jugador con el mouse."""
    def __init__(self, model):
        self.model = model

    def get_left(self):
        x, _ = pygame.mouse.get_pos()
        return x < self.model.player.x - 10  # se mueve si el mouse está a la izquierda

    def get_right(self):
        x, _ = pygame.mouse.get_pos()
        return x > self.model.player.x + 10  # se mueve si el mouse está a la derecha

    def get_jump(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # clic izquierdo
                return True
        return False
# --------------------------


class Controlador:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.model = Modelo()
        self.vista = Vista(self.model)
        self.running = True

        # 🔸 NUEVO: Usamos el adaptador del mouse
        self.input_adapter = MouseAdapter(self.model)

    def handle_input(self, events):
        player = self.model.player
        speed = player.get_speed()

        # 🔸 NUEVO: Movimiento basado en mouse
        if self.input_adapter.get_left():
            player.vx = -speed
            player.moving = True
            player.facing = "left"
        elif self.input_adapter.get_right():
            player.vx = speed
            player.moving = True
            player.facing = "right"
        else:
            player.vx = 0
            player.moving = False

        # 🔸 NUEVO: Salto con clic izquierdo
        if self.input_adapter.get_jump(events):
            player.jump()

    def update_active_buffs_list(self):
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
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.handle_input(events)
            self.model.update(dt)
            player_rect = self.model.get_player_rect()
            self.model.pickup_item_if_collide(player_rect)
            self.update_active_buffs_list()
            self.vista.draw(dt)

        pygame.quit()
