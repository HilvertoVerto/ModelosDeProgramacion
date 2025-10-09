"""Controlador del juego - Patrón MVC + Adapter"""
import pygame
from v.Vista import Vista
from m.Modelo import Modelo
from c.InputAdapter import InputManager


class Controlador:
    """Controlador principal - Maneja input y coordina Modelo-Vista"""
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.model = Modelo()
        self.vista = Vista(self.model)
        self.input_manager = InputManager()  # Patrón Adapter
        self.running = True
        
        print("Modo TECLADO activado (default)")
        print("Presiona P para alternar entre Teclado y Mouse")

    def handle_input(self, events):
        """Procesa entrada del usuario usando el patrón Adapter"""
        player = self.model.player
        
        # Verificar si se presionó P para cambiar modo
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                self.input_manager.toggle_input_mode()
        
        # Obtener movimiento del adaptador actual
        vx, moving, facing = self.input_manager.get_movement(player)
        player.vx = vx
        player.moving = moving
        player.facing = facing
        
        # Verificar salto con el adaptador actual
        self.input_manager.check_jump(events, player)

    def run(self):
        """Bucle principal del juego"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
            
            self.handle_input(events)
            self.model.update(dt)
            self.vista.draw(dt, self.input_manager.get_current_mode())
        
        pygame.quit()