import pygame
import os

SCREEN_W, SCREEN_H = 800, 600
GROUND_Y = 520  # Mismo valor que en Modelo

def load_image(path):
    return pygame.image.load(path).convert_alpha()

class Vista:
    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Don Armando - Buffs Activos")

        # Cargar fondo
        self.background = None
        self.load_background()

        # Carga íconos de buffs
        self.buff_icons = {}
        self.load_icons()

        self.font = pygame.font.SysFont("Arial", 20)

    def load_background(self):
        """Carga la imagen de fondo"""
        try:
            bg_path = os.path.join("graficos", "Fondo", "Fondo.png")
            self.background = pygame.image.load(bg_path).convert()
            # Escalar al tamaño de la pantalla si es necesario
            self.background = pygame.transform.scale(self.background, (SCREEN_W, SCREEN_H))
            print("✓ Fondo cargado correctamente")
        except Exception as e:
            print(f"⚠ No se pudo cargar el fondo: {e}")
            print("  Se usará color sólido como respaldo")
            self.background = None

    def load_icons(self):
        """Carga los íconos de los buffs desde la carpeta Bufos"""
        icon_folder = os.path.join("graficos", "Bufos")
        
        # Mapeo de buffs a archivos
        icon_files = {
            "forehead": "Buff_Frente.png",
            "vestido": "Buff_Ropa.png",
            "caballeria": "Buff_Ropa.png",  # Usa el mismo ícono de ropa
            "speed": "Buff_Correr.png"
        }
        
        self.buff_icons = {}
        
        for key, fname in icon_files.items():
            path = os.path.join(icon_folder, fname)
            try:
                icon = load_image(path)
                self.buff_icons[key] = icon
                print(f"✓ Ícono cargado: {fname}")
            except Exception as e:
                print(f"⚠ No se pudo cargar {fname}: {e}")
                # Ícono de respaldo con colores originales
                surf = pygame.Surface((32, 32))
                if key == "forehead":
                    surf.fill((0, 200, 255))  # Cyan
                elif key in ["vestido", "caballeria"]:
                    surf.fill((255, 0, 255))  # Magenta
                else:  # speed
                    surf.fill((255, 255, 0))  # Amarillo
                self.buff_icons[key] = surf

    def draw_ground(self):
        """Dibuja el suelo en la parte inferior"""
        pygame.draw.rect(self.screen, (100, 180, 100), (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))

    def draw_player(self, dt):
        p = self.model.player
        sprite = p.get_sprite(dt)
        self.screen.blit(sprite, (int(p.x), int(p.y)))

    def draw_buffs(self):
        """Dibuja los buffs activos en pantalla con barras de tiempo."""
        import time
        
        x_start, y_start = 10, 10
        icon_size = 50  # Aumentado de 40 a 50
        bar_width = 100
        bar_height = 8
        spacing = 10
        border_radius = 8  # Radio para esquinas redondeadas
        
        bm = self.model.buff_manager
        current_time = time.time()
        buff_index = 0
        
        # Buff de Frente
        if bm.front_level > 0 and bm.front_expire > 0:
            x = x_start
            y = y_start + (buff_index * (icon_size + bar_height + spacing + 5))
            
            # Dibujar borde negro con esquinas redondeadas
            border_rect = pygame.Rect(x - 3, y - 3, icon_size + 6, icon_size + 6)
            pygame.draw.rect(self.screen, (0, 0, 0), border_rect, border_radius=border_radius)
            
            # Dibujar fondo blanco para el ícono
            icon_bg_rect = pygame.Rect(x, y, icon_size, icon_size)
            pygame.draw.rect(self.screen, (255, 255, 255), icon_bg_rect, border_radius=border_radius - 2)
            
            # Dibujar ícono
            icon = self.buff_icons.get("forehead")
            if icon:
                icon_scaled = pygame.transform.scale(icon, (icon_size - 6, icon_size - 6))
                self.screen.blit(icon_scaled, (x + 3, y + 3))
            else:
                pygame.draw.rect(self.screen, (0, 200, 255), (x + 3, y + 3, icon_size - 6, icon_size - 6), border_radius=border_radius - 3)
            
            # Calcular tiempo restante
            time_remaining = max(0, bm.front_expire - current_time)
            progress = time_remaining / 10.0
            
            # Dibujar barra de fondo
            bar_x = x + icon_size + 10
            bar_y = y + (icon_size - bar_height) // 2
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Dibujar barra de progreso (verde -> amarillo -> rojo según tiempo)
            if progress > 0:
                if progress > 0.5:
                    color = (0, 255, 0)  # Verde
                elif progress > 0.25:
                    color = (255, 255, 0)  # Amarillo
                else:
                    color = (255, 0, 0)  # Rojo
                    
                pygame.draw.rect(self.screen, color, 
                               (bar_x, bar_y, int(bar_width * progress), bar_height))
            
            # Texto de nivel y tiempo
            text = f"Frente x{bm.front_level} - {int(time_remaining)}s"
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (bar_x + bar_width + 10, bar_y - 3))
            
            buff_index += 1
        
        # Buff de Ropa
        if bm.clothes_type != "traje" and bm.clothes_expire > 0:
            x = x_start
            y = y_start + (buff_index * (icon_size + bar_height + spacing + 5))
            
            # Dibujar borde negro con esquinas redondeadas
            border_rect = pygame.Rect(x - 3, y - 3, icon_size + 6, icon_size + 6)
            pygame.draw.rect(self.screen, (0, 0, 0), border_rect, border_radius=border_radius)
            
            # Dibujar fondo blanco para el ícono
            icon_bg_rect = pygame.Rect(x, y, icon_size, icon_size)
            pygame.draw.rect(self.screen, (255, 255, 255), icon_bg_rect, border_radius=border_radius - 2)
            
            # Dibujar ícono
            icon_key = bm.clothes_type
            icon = self.buff_icons.get(icon_key)
            if icon:
                icon_scaled = pygame.transform.scale(icon, (icon_size - 6, icon_size - 6))
                self.screen.blit(icon_scaled, (x + 3, y + 3))
            else:
                pygame.draw.rect(self.screen, (255, 0, 255), (x + 3, y + 3, icon_size - 6, icon_size - 6), border_radius=border_radius - 3)
            
            # Calcular tiempo restante
            time_remaining = max(0, bm.clothes_expire - current_time)
            progress = time_remaining / 10.0
            
            # Dibujar barra de fondo
            bar_x = x + icon_size + 10
            bar_y = y + (icon_size - bar_height) // 2
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Dibujar barra de progreso (verde -> amarillo -> rojo según tiempo)
            if progress > 0:
                if progress > 0.5:
                    color = (0, 255, 0)  # Verde
                elif progress > 0.25:
                    color = (255, 255, 0)  # Amarillo
                else:
                    color = (255, 0, 0)  # Rojo
                    
                pygame.draw.rect(self.screen, color, 
                               (bar_x, bar_y, int(bar_width * progress), bar_height))
            
            # Texto
            clothes_name = "Vestido" if bm.clothes_type == "vestido" else "Caballería"
            text = f"{clothes_name} - {int(time_remaining)}s"
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (bar_x + bar_width + 10, bar_y - 3))
            
            buff_index += 1
        
        # Buff de Velocidad
        if bm.speed_level > 0 and bm.speed_expire > 0:
            x = x_start
            y = y_start + (buff_index * (icon_size + bar_height + spacing + 5))
            
            # Dibujar borde negro con esquinas redondeadas
            border_rect = pygame.Rect(x - 3, y - 3, icon_size + 6, icon_size + 6)
            pygame.draw.rect(self.screen, (0, 0, 0), border_rect, border_radius=border_radius)
            
            # Dibujar fondo blanco para el ícono
            icon_bg_rect = pygame.Rect(x, y, icon_size, icon_size)
            pygame.draw.rect(self.screen, (255, 255, 255), icon_bg_rect, border_radius=border_radius - 2)
            
            # Dibujar ícono
            icon = self.buff_icons.get("speed")
            if icon:
                icon_scaled = pygame.transform.scale(icon, (icon_size - 6, icon_size - 6))
                self.screen.blit(icon_scaled, (x + 3, y + 3))
            else:
                pygame.draw.rect(self.screen, (255, 255, 0), (x + 3, y + 3, icon_size - 6, icon_size - 6), border_radius=border_radius - 3)
            
            # Calcular tiempo restante
            time_remaining = max(0, bm.speed_expire - current_time)
            progress = time_remaining / 10.0
            
            # Dibujar barra de fondo
            bar_x = x + icon_size + 10
            bar_y = y + (icon_size - bar_height) // 2
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Dibujar barra de progreso (verde -> amarillo -> rojo según tiempo)
            if progress > 0:
                if progress > 0.5:
                    color = (0, 255, 0)  # Verde
                elif progress > 0.25:
                    color = (255, 255, 0)  # Amarillo
                else:
                    color = (255, 0, 0)  # Rojo
                    
                pygame.draw.rect(self.screen, color, 
                               (bar_x, bar_y, int(bar_width * progress), bar_height))
            
            # Texto con multiplicador real
            speed_mult = bm.get_speed_multiplier()
            text = f"Velocidad x{speed_mult:.1f} (Nivel {bm.speed_level}) - {int(time_remaining)}s"
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (bar_x + bar_width + 10, bar_y - 3))
            
            buff_index += 1

    def draw_items(self):
        """Dibuja los ítems en el suelo usando los íconos de buffs con borde"""
        icon_size = 50  # Mismo tamaño que los buffs
        border_radius = 8
        
        for it in self.model.items_on_floor:
            x, y = it["x"], it["y"]
            
            # Dibujar borde negro con esquinas redondeadas
            border_rect = pygame.Rect(x - 3, y - 3, icon_size + 6, icon_size + 6)
            pygame.draw.rect(self.screen, (0, 0, 0), border_rect, border_radius=border_radius)
            
            # Dibujar fondo blanco para el ícono
            icon_bg_rect = pygame.Rect(x, y, icon_size, icon_size)
            pygame.draw.rect(self.screen, (255, 255, 255), icon_bg_rect, border_radius=border_radius - 2)
            
            # Obtener el ícono correspondiente
            if it["type"] == "clothes":
                icon = self.buff_icons.get("vestido")
            elif it["type"] == "forehead":
                icon = self.buff_icons.get("forehead")
            elif it["type"] == "speed":
                icon = self.buff_icons.get("speed")
            else:
                icon = None
            
            # Dibujar el ícono escalado
            if icon:
                icon_scaled = pygame.transform.scale(icon, (icon_size - 6, icon_size - 6))
                self.screen.blit(icon_scaled, (x + 3, y + 3))
            else:
                # Respaldo con cuadrados de colores
                if it["type"] == "clothes":
                    color = (255, 0, 255)  # Magenta
                elif it["type"] == "forehead":
                    color = (0, 200, 255)  # Cyan
                elif it["type"] == "speed":
                    color = (255, 255, 0)  # Amarillo
                pygame.draw.rect(self.screen, color, (x + 3, y + 3, icon_size - 6, icon_size - 6), 
                               border_radius=border_radius - 3)

    def draw(self, dt):
        # Dibujar fondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Color de respaldo si no hay imagen
            self.screen.fill((30, 30, 40))
        
        self.draw_ground()
        self.draw_items()
        self.draw_player(dt)
        self.draw_buffs()
        
        # DEBUG: Mostrar posición y dimensiones del jugador
        p = self.model.player
        debug_text = f"Y: {int(p.y)} | H: {int(p.sprite_height)} | Ground: {GROUND_Y} | Límite: {int(GROUND_Y - p.sprite_height)}"
        debug_label = self.font.render(debug_text, True, (255, 255, 0))
        self.screen.blit(debug_label, (10, SCREEN_H - 30))
        
        pygame.display.flip()