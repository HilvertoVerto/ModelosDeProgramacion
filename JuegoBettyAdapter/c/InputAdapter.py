"""Patrón Adapter para diferentes tipos de input"""
import pygame
from abc import ABC, abstractmethod


class InputInterface(ABC):
    """Interfaz abstracta para sistemas de input"""
    
    @abstractmethod
    def get_movement(self, player):
        """
        Retorna la velocidad horizontal deseada y si está en movimiento.
        Returns: (vx, moving, facing)
        """
        pass
    
    @abstractmethod
    def check_jump(self, events, player):
        """Verifica si el jugador debe saltar"""
        pass


class KeyboardAdapter(InputInterface):
    """Adaptador para input de teclado (original)"""
    
    def get_movement(self, player):
        """Procesa movimiento con teclado"""
        keys = pygame.key.get_pressed()
        speed = player.get_speed()
        
        if keys[pygame.K_LEFT]:
            return -speed, True, "left"
        elif keys[pygame.K_RIGHT]:
            return speed, True, "right"
        else:
            return 0, False, player.facing
    
    def check_jump(self, events, player):
        """Salto con tecla espacio"""
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                player.jump()
                return True
        return False


class MouseAdapter(InputInterface):
    """Adaptador para input de mouse"""
    
    def __init__(self):
        self.target_x = None  # Posición objetivo del click
        self.movement_threshold = 5  # Píxeles mínimos para considerar que llegó
    
    def get_movement(self, player):
        """Procesa movimiento con mouse (click izquierdo)"""
        # Si hay un objetivo activo
        if self.target_x is not None:
            distance = self.target_x - player.x
            
            # Si llegó al objetivo (dentro del threshold)
            if abs(distance) <= self.movement_threshold:
                self.target_x = None
                return 0, False, player.facing
            
            # Moverse hacia el objetivo
            speed = player.get_speed()
            if distance < 0:
                return -speed, True, "left"
            else:
                return speed, True, "right"
        
        return 0, False, player.facing
    
    def check_jump(self, events, player):
        """Salto con click derecho"""
        for e in events:
            # Click izquierdo: establecer objetivo de movimiento
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # Click izquierdo
                self.target_x = e.pos[0]
                return False
            
            # Click derecho: saltar
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:  # Click derecho
                player.jump()
                return True
        
        return False
    
    def cancel_movement(self):
        """Cancela el movimiento actual"""
        self.target_x = None


class InputManager:
    """Gestor que alterna entre diferentes adaptadores de input"""
    
    def __init__(self):
        self.keyboard_adapter = KeyboardAdapter()
        self.mouse_adapter = MouseAdapter()
        self.current_adapter = self.keyboard_adapter
        self.input_mode = "keyboard"  # "keyboard" o "mouse"
    
    def toggle_input_mode(self):
        """Alterna entre teclado y mouse (tecla P)"""
        if self.input_mode == "keyboard":
            self.input_mode = "mouse"
            self.current_adapter = self.mouse_adapter
            print("Modo MOUSE activado: Click izquierdo = mover, Click derecho = saltar")
        else:
            self.input_mode = "keyboard"
            self.current_adapter = self.keyboard_adapter
            self.mouse_adapter.cancel_movement()  # Cancelar movimiento pendiente
            print("Modo TECLADO activado: Flechas = mover, Espacio = saltar")
    
    def get_movement(self, player):
        """Delega al adaptador actual"""
        return self.current_adapter.get_movement(player)
    
    def check_jump(self, events, player):
        """Delega al adaptador actual"""
        return self.current_adapter.check_jump(events, player)
    
    def get_current_mode(self):
        """Retorna el modo actual"""
        return self.input_mode