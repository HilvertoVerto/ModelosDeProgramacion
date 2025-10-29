import pygame
import sys
from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum

# ============================================
# PATRÓN COMMAND - Cada acción es un comando
# Principio SOLID: Single Responsibility - cada comando hace UNA cosa
# ============================================

class Command(ABC):
    """Interfaz base para comandos (Interface Segregation Principle)"""
    
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def undo(self) -> str:
        pass


class AttackCommand(Command):
    """Comando concreto: Ataque"""
    
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.damage_dealt = 0
        self.previous_defense = defender.defense
    
    def execute(self) -> str:
        # El daño se reduce por la defensa
        base_damage = 20
        self.damage_dealt = max(5, base_damage - self.previous_defense)
        self.defender.hp -= self.damage_dealt
        self.defender.defense = 0  # La defensa se resetea después del ataque
        return f"{self.attacker.name} ataca causando {self.damage_dealt} de daño!"
    
    def undo(self) -> str:
        self.defender.hp += self.damage_dealt
        self.defender.defense = self.previous_defense
        return f"Deshaciendo ataque"


class DefendCommand(Command):
    """Comando concreto: Defender"""
    
    def __init__(self, character):
        self.character = character
        self.previous_defense = 0
    
    def execute(self) -> str:
        self.previous_defense = self.character.defense
        self.character.defense = 10
        return f"{self.character.name} se defiende! (Defensa: {self.character.defense})"
    
    def undo(self) -> str:
        self.character.defense = self.previous_defense
        return "Defensa cancelada"


class HealCommand(Command):
    """Comando concreto: Curar"""
    
    def __init__(self, character):
        self.character = character
        self.healed_amount = 0
    
    def execute(self) -> str:
        self.healed_amount = min(30, 100 - self.character.hp)
        self.character.hp = min(100, self.character.hp + 30)
        self.character.potions -= 1
        return f"{self.character.name} se cura {self.healed_amount} HP!"
    
    def undo(self) -> str:
        self.character.hp -= self.healed_amount
        self.character.potions += 1
        return "Curación deshecha"


# ============================================
# PATRÓN CHAIN OF RESPONSIBILITY
# Principio SOLID: Open/Closed - puedes agregar handlers sin modificar existentes
# ============================================

class Handler(ABC):
    """Interfaz base para manejadores"""
    
    def __init__(self):
        self._next_handler: Optional[Handler] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, command: Command) -> tuple[bool, str]:
        pass


class AliveCheckHandler(Handler):
    """Valida que el personaje esté vivo"""
    
    def handle(self, command: Command) -> tuple[bool, str]:
        if hasattr(command, 'attacker') and command.attacker.hp <= 0:
            return False, f"{command.attacker.name} está muerto!"
        
        if hasattr(command, 'character') and command.character.hp <= 0:
            return False, f"{command.character.name} está muerto!"
        
        if self._next_handler:
            return self._next_handler.handle(command)
        return True, "OK"


class ResourceCheckHandler(Handler):
    """Valida recursos disponibles"""
    
    def handle(self, command: Command) -> tuple[bool, str]:
        if isinstance(command, HealCommand):
            if command.character.potions <= 0:
                return False, "¡No tienes pociones!"
            if command.character.hp >= 100:
                return False, "¡HP al máximo!"
        
        if self._next_handler:
            return self._next_handler.handle(command)
        return True, "OK"


class ExecutionHandler(Handler):
    """Ejecuta el comando después de validaciones"""
    
    def handle(self, command: Command) -> tuple[bool, str]:
        result = command.execute()
        return True, result


# ============================================
# ENTIDADES - Principio SOLID: Single Responsibility
# ============================================

class Character:
    """Representa un personaje del juego"""
    
    def __init__(self, name: str, x: int, y: int, color: tuple):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.defense = 0
        self.potions = 3
        self.x = x
        self.y = y
        self.color = color
    
    def is_alive(self) -> bool:
        return self.hp > 0


# ============================================
# CONTROLADOR - Principio SOLID: Dependency Inversion
# Depende de abstracciones (Command, Handler) no de implementaciones concretas
# ============================================

class GameController:
    """Controla la lógica del juego"""
    
    def __init__(self):
        self.command_history: List[Command] = []
        
        # Configurar cadena de responsabilidad
        self.chain = AliveCheckHandler()
        self.chain.set_next(ResourceCheckHandler()).set_next(ExecutionHandler())
    
    def execute_command(self, command: Command) -> tuple[bool, str]:
        success, message = self.chain.handle(command)
        
        if success:
            self.command_history.append(command)
        
        return success, message
    
    def undo_last_command(self) -> str:
        if not self.command_history:
            return "No hay acciones para deshacer"
        
        last_command = self.command_history.pop()
        return last_command.undo()


# ============================================
# VISTA - Interfaz gráfica con Pygame
# Principio SOLID: Single Responsibility - solo maneja UI
# ============================================

class GameView:
    """Maneja la visualización del juego"""
    
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RPG - Command & Chain of Responsibility")
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
    
    def draw_character(self, character: Character, is_player: bool):
        """Dibuja un personaje en pantalla"""
        # Cuerpo
        pygame.draw.circle(self.screen, character.color, (character.x, character.y), 40)
        
        # Nombre
        name_text = self.small_font.render(character.name, True, (255, 255, 255))
        self.screen.blit(name_text, (character.x - 40, character.y - 80))
        
        # Barra de HP
        hp_bar_width = 80
        hp_bar_height = 10
        hp_percentage = character.hp / character.max_hp
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(self.screen, (100, 0, 0), 
                        (character.x - 40, character.y + 50, hp_bar_width, hp_bar_height))
        # HP actual (verde)
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        (character.x - 40, character.y + 50, int(hp_bar_width * hp_percentage), hp_bar_height))
        
        # Texto HP
        hp_text = self.small_font.render(f"HP: {character.hp}/{character.max_hp}", True, (255, 255, 255))
        self.screen.blit(hp_text, (character.x - 40, character.y + 65))
        
        # Defensa si está activa
        if character.defense > 0:
            def_text = self.small_font.render(f"DEF: {character.defense}", True, (100, 150, 255))
            self.screen.blit(def_text, (character.x - 40, character.y + 85))
        
        # Pociones si es jugador
        if is_player:
            pot_text = self.small_font.render(f"Pociones: {character.potions}", True, (255, 200, 0))
            self.screen.blit(pot_text, (character.x - 40, character.y + 105))
    
    def draw_buttons(self):
        """Dibuja los botones de acción"""
        buttons = [
            ("Q - Atacar", 50, 500),
            ("W - Defender", 200, 500),
            ("E - Curar", 380, 500),
            ("R - Deshacer", 520, 500)
        ]
        
        for text, x, y in buttons:
            button_text = self.small_font.render(text, True, (255, 255, 255))
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 120, 40))
            self.screen.blit(button_text, (x + 10, y + 10))
    
    def draw_message(self, message: str):
        """Dibuja el mensaje de acción"""
        if message:
            msg_text = self.small_font.render(message, True, (255, 255, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 400, 700, 50))
            self.screen.blit(msg_text, (60, 410))
    
    def draw(self, player: Character, enemy: Character, message: str):
        """Dibuja toda la escena"""
        self.screen.fill((20, 20, 40))
        
        # Título
        title = self.font.render("RPG - Patrones de Diseño", True, (255, 255, 255))
        self.screen.blit(title, (200, 20))
        
        self.draw_character(player, True)
        self.draw_character(enemy, False)
        self.draw_buttons()
        self.draw_message(message)
        
        pygame.display.flip()
        self.clock.tick(60)


# ============================================
# JUEGO PRINCIPAL
# ============================================

class Game:
    """Clase principal que une todo"""
    
    def __init__(self):
        self.view = GameView()
        self.controller = GameController()
        
        # Crear personajes
        self.player = Character("Jugador", 200, 250, (0, 200, 255))
        self.enemy = Character("Enemigo", 600, 250, (255, 50, 50))
        
        self.message = "¡Presiona Q, W, E para actuar! R para deshacer"
        self.running = True
    
    def enemy_ai(self):
        """IA simple del enemigo - solo ataca"""
        if self.enemy.is_alive():
            cmd = AttackCommand(self.enemy, self.player)
            success, msg = self.controller.execute_command(cmd)
            if success:
                self.message = f"ENEMIGO: {msg}"
    
    def handle_input(self, event):
        """Maneja input del jugador"""
        if event.type == pygame.KEYDOWN:
            # Q - Atacar
            if event.key == pygame.K_q:
                cmd = AttackCommand(self.player, self.enemy)
                success, msg = self.controller.execute_command(cmd)
                self.message = msg
                if success:
                    pygame.time.wait(500)
                    self.enemy_ai()
            
            # W - Defender
            elif event.key == pygame.K_w:
                cmd = DefendCommand(self.player)
                success, msg = self.controller.execute_command(cmd)
                self.message = msg
                if success:
                    pygame.time.wait(500)
                    self.enemy_ai()
            
            # E - Curar
            elif event.key == pygame.K_e:
                cmd = HealCommand(self.player)
                success, msg = self.controller.execute_command(cmd)
                self.message = msg
                if success:
                    pygame.time.wait(500)
                    self.enemy_ai()
            
            # R - Deshacer
            elif event.key == pygame.K_r:
                msg = self.controller.undo_last_command()
                self.message = f"DESHACER: {msg}"
        
        # Verificar fin del juego
        if not self.player.is_alive():
            self.message = "¡HAS PERDIDO! Cierra la ventana"
        elif not self.enemy.is_alive():
            self.message = "¡HAS GANADO! Cierra la ventana"
    
    def run(self):
        """Loop principal del juego"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)
            
            self.view.draw(self.player, self.enemy, self.message)
        
        pygame.quit()
        sys.exit()


# ============================================
# EJECUTAR JUEGO
# ============================================

if __name__ == "__main__":
    game = Game()
    game.run()