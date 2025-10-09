"""Renderizador de interfaz de usuario"""
import pygame
import time
from m.Constants import ICON_SIZE, BORDER_WIDTH


class UIRenderer:
    """Renderiza elementos de UI: buffs, barras, debug info"""
    
    def __init__(self, screen, buff_icons, font):
        self.screen = screen
        self.buff_icons = buff_icons
        self.font = font

    def draw_buffs(self, buff_manager):
        """Dibuja buffs activos con barras de tiempo"""
        x_start, y_start = 10, 10
        bar_width, bar_height, spacing = 100, 8, 10
        current_time = time.time()
        buff_index = 0
        
        # Buff de Frente
        if buff_manager.front_level > 0 and buff_manager.front_expire > 0:
            y = y_start + (buff_index * (ICON_SIZE + bar_height + spacing + 5))
            self._draw_buff_icon(x_start, y, "forehead", (0, 200, 255))
            self._draw_buff_bar(x_start, y, buff_manager.front_expire, current_time, bar_width, bar_height)
            self._draw_buff_text(x_start, y, f"Frente x{buff_manager.front_level}", 
                               buff_manager.front_expire, current_time, bar_width, bar_height)
            buff_index += 1
        
        # Buff de Ropa
        if buff_manager.clothes_type != "traje" and buff_manager.clothes_expire > 0:
            y = y_start + (buff_index * (ICON_SIZE + bar_height + spacing + 5))
            self._draw_buff_icon(x_start, y, buff_manager.clothes_type, (255, 0, 255))
            self._draw_buff_bar(x_start, y, buff_manager.clothes_expire, current_time, bar_width, bar_height)
            clothes_name = "Vestido" if buff_manager.clothes_type == "vestido" else "Caballería"
            self._draw_buff_text(x_start, y, clothes_name, 
                               buff_manager.clothes_expire, current_time, bar_width, bar_height)
            buff_index += 1
        
        # Buff de Velocidad
        if buff_manager.speed_level > 0 and buff_manager.speed_expire > 0:
            y = y_start + (buff_index * (ICON_SIZE + bar_height + spacing + 5))
            self._draw_buff_icon(x_start, y, "speed", (255, 255, 0))
            self._draw_buff_bar(x_start, y, buff_manager.speed_expire, current_time, bar_width, bar_height)
            speed_mult = buff_manager.get_speed_multiplier()
            self._draw_buff_text(x_start, y, f"Velocidad x{speed_mult:.1f} (Nivel {buff_manager.speed_level})", 
                               buff_manager.speed_expire, current_time, bar_width, bar_height)

    def _draw_buff_icon(self, x, y, icon_key, fallback_color):
        """Dibuja ícono de buff con borde interno y esquinas redondeadas"""
        border_radius = 8  # Radio de las esquinas redondeadas
        
        # Fondo blanco con esquinas redondeadas
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
        
        # Obtener y dibujar ícono
        icon = self.buff_icons.get(icon_key)
        if icon:
            # Escalar ícono
            icon_scaled = pygame.transform.scale(icon, (ICON_SIZE, ICON_SIZE))
            
            # Crear superficie con transparencia para recortar esquinas
            icon_surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
            
            # Dibujar máscara de esquinas redondeadas
            pygame.draw.rect(icon_surface, (255, 255, 255, 255), (0, 0, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
            
            # Aplicar ícono con máscara
            icon_surface.blit(icon_scaled, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self.screen.blit(icon_surface, (x, y))
        else:
            # Color de respaldo con esquinas redondeadas
            pygame.draw.rect(self.screen, fallback_color, (x, y, ICON_SIZE, ICON_SIZE), border_radius=border_radius)
        
        # Borde negro POR DENTRO con esquinas redondeadas
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, ICON_SIZE, ICON_SIZE), BORDER_WIDTH, border_radius=border_radius)

    def _draw_buff_bar(self, x, y, expire_time, current_time, bar_width, bar_height):
        """Dibuja barra de progreso"""
        time_remaining = max(0, expire_time - current_time)
        progress = time_remaining / 10.0
        bar_x = x + ICON_SIZE + 10
        bar_y = y + (ICON_SIZE - bar_height) // 2
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        if progress > 0:
            if progress > 0.5:
                color = (0, 255, 0)
            elif progress > 0.25:
                color = (255, 255, 0)
            else:
                color = (255, 0, 0)
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, int(bar_width * progress), bar_height))

    def _draw_buff_text(self, x, y, text, expire_time, current_time, bar_width, bar_height):
        """Dibuja texto del buff"""
        time_remaining = max(0, expire_time - current_time)
        full_text = f"{text} - {int(time_remaining)}s"
        label = self.font.render(full_text, True, (255, 255, 255))
        bar_x = x + ICON_SIZE + 10
        bar_y = y + (ICON_SIZE - bar_height) // 2
        self.screen.blit(label, (bar_x + bar_width + 10, bar_y - 3))

    def draw_debug_info(self, player, ground_y, screen_h, input_mode=None):
        """Dibuja información de debug"""
        debug_text = f"Y: {int(player.y)} | H: {int(player.sprite_height)} | Ground: {ground_y} | Límite: {int(ground_y - player.sprite_height)}"
        debug_label = self.font.render(debug_text, True, (255, 255, 0))
        self.screen.blit(debug_label, (10, screen_h - 30))
        
        # Mostrar modo de input actual
        if input_mode:
            mode_text = "  TECLADO" if input_mode == "keyboard" else "  MOUSE"
            mode_color = (100, 255, 100) if input_mode == "keyboard" else (100, 200, 255)
            mode_label = self.font.render(f"Modo: {mode_text} (P para cambiar)", True, mode_color)
            self.screen.blit(mode_label, (10, screen_h - 55))