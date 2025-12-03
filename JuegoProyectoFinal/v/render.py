import os
import pygame
from v.sprite_manager import SpriteManager


class Render:
    """Clase encargada de renderizar los elementos del juego"""

    def __init__(self, ventana, ancho, alto, altura_suelo=50, fondo=None):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto

        # Colores
        self.AZUL_CIELO = (135, 206, 235)
        self.VERDE = (34, 139, 34)
        self.MARRON = (139, 69, 19)
        self.TIERRA = (150, 111, 51)
        self.ROJO_ENEMIGO = (200, 60, 60)
        self.AZUL_BUFF = (70, 130, 180)
        self.AMARILLO_BUFF = (255, 215, 0)
        self.VERDE_BUFF = (60, 179, 113)
        self.MORADO_META = (138, 43, 226)
        self.TEXT_COLOR = (20, 20, 20)
        self.HUD_BG = (255, 255, 255)
        self.BARRA_FONDO = (220, 220, 220)
        self.BARRA_BORDE = (80, 80, 80)

        # Altura del suelo
        self.altura_suelo = altura_suelo

        # Fondo
        self.fondo_path = fondo
        self.fondo_imagen = None
        self.fondo_ancho = 0
        self.fondo_x = 0  # Posicion x del fondo para scrolling
        self.cargar_fondo()

        # Camara
        self.camara_x = 0

        # HUD
        self.hud_font = pygame.font.SysFont("arial", 18)

        # Sprite Manager
        self.sprite_manager = SpriteManager()
        self.sprite_manager.cargar_todos()

    def cargar_fondo(self):
        """Carga la imagen de fondo si existe"""
        fondo_path = self.fondo_path or os.path.join("graficos", "Fondo", "Fondo.png")
        if os.path.exists(fondo_path):
            self.fondo_imagen = pygame.image.load(fondo_path).convert()
            # Escalar el fondo a la altura de la ventana manteniendo proporcion
            self.fondo_imagen = pygame.transform.scale(
                self.fondo_imagen,
                (
                    int(self.fondo_imagen.get_width() * self.alto / self.fondo_imagen.get_height()),
                    self.alto,
                ),
            )
            self.fondo_ancho = self.fondo_imagen.get_width()

    def limpiar_pantalla(self):
        """Limpia la pantalla con el color de fondo"""
        if self.fondo_imagen:
            # Dibujar fondo con scrolling infinito
            # Normalizar la posicion x para que este siempre entre 0 y fondo_ancho
            parallax = 0.5
            self.fondo_x = int(self.camara_x * parallax) % self.fondo_ancho

            # Dibujar dos copias del fondo para crear efecto infinito
            self.ventana.blit(self.fondo_imagen, (-self.fondo_x, 0))
            self.ventana.blit(self.fondo_imagen, (self.fondo_ancho - self.fondo_x, 0))
        else:
            # Fallback al color azul si no hay imagen
            self.ventana.fill(self.AZUL_CIELO)

    def dibujar_suelo(self):
        """Dibuja el suelo del juego"""
        pygame.draw.rect(
            self.ventana,
            self.VERDE,
            (0, self.alto - self.altura_suelo, self.ancho, self.altura_suelo),
        )

        pygame.draw.line(
            self.ventana,
            self.MARRON,
            (0, self.alto - self.altura_suelo),
            (self.ancho, self.alto - self.altura_suelo),
            3,
        )

    def dibujar_plataformas(self, plataformas):
        """Dibuja plataformas rectangulares del nivel"""
        for plataforma in plataformas:
            desplazado = plataforma.move(-self.camara_x, 0)
            pygame.draw.rect(self.ventana, self.TIERRA, desplazado, border_radius=8)

    def dibujar_enemigos(self, enemigos):
        """Dibuja enemigos usando sus sprites"""
        for enemigo in enemigos:
            desplazado = enemigo.rect.move(-self.camara_x, 0)

            # Obtener sprite según tipo de arma
            arma = getattr(enemigo, "arma", None)
            tipo_arma = arma.nombre if arma else "Espada"
            sprite = self.sprite_manager.get_sprite_enemigo(tipo_arma)

            if sprite:
                # Dibujar sprite centrado en la posición del enemigo
                sprite_rect = sprite.get_rect(center=desplazado.center)
                self.ventana.blit(sprite, sprite_rect)
            else:
                # Fallback: rectángulo de color
                color = getattr(enemigo, "color", self.ROJO_ENEMIGO)
                pygame.draw.rect(self.ventana, color, desplazado, border_radius=8)
                pygame.draw.rect(self.ventana, self.MARRON, desplazado, width=1, border_radius=8)

    def dibujar_buffos(self, buffos):
        """Dibuja buffos coleccionables usando sprites"""
        for buffo in buffos:
            desplazado = buffo.rect.move(-self.camara_x, 0)

            # Obtener sprite según tipo de buff
            sprite = self.sprite_manager.get_sprite_buff(buffo.tipo)

            if sprite:
                # Dibujar sprite centrado en la posición del buff
                sprite_rect = sprite.get_rect(center=desplazado.center)
                self.ventana.blit(sprite, sprite_rect)
            else:
                # Fallback: círculo de color
                colores = {
                    "velocidad": self.AMARILLO_BUFF,
                    "salto": self.AZUL_BUFF,
                    "invencible": self.VERDE_BUFF,
                }
                color = colores.get(buffo.tipo, self.AMARILLO_BUFF)
                centro = desplazado.center
                radio = max(6, min(desplazado.width, desplazado.height) // 2)
                pygame.draw.circle(self.ventana, color, centro, radio)
                pygame.draw.circle(self.ventana, self.BARRA_BORDE, centro, radio, width=1)

    def dibujar_meta(self, meta_x):
        """Dibuja una meta vertical simple al final del mapa"""
        x = int(meta_x - self.camara_x)
        if -10 <= x <= self.ancho + 10:
            pygame.draw.rect(self.ventana, self.MORADO_META, (x, 0, 6, self.alto))

    def dibujar_proyectiles(self, proyectiles):
        """Dibuja proyectiles usando sprites"""
        for proyectil in proyectiles:
            if not proyectil.vivo:
                continue
            desplazado = proyectil.rect.move(-self.camara_x, 0)

            # Obtener sprite según dirección del proyectil
            direccion = 1 if proyectil.vx > 0 else -1
            sprite = self.sprite_manager.get_sprite_proyectil(direccion)

            if sprite:
                # Dibujar sprite centrado en la posición del proyectil
                sprite_rect = sprite.get_rect(center=desplazado.center)
                self.ventana.blit(sprite, sprite_rect)
            else:
                # Fallback: rectángulo de color
                pygame.draw.rect(self.ventana, proyectil.color, desplazado, border_radius=4)
                pygame.draw.rect(self.ventana, self.BARRA_BORDE, desplazado, width=1, border_radius=4)

    def dibujar_buff_timers(self, buff_timers):
        """HUD de temporizadores de buffos con barra y texto."""
        if not buff_timers:
            return
        x = 10
        y = 10
        barra_ancho = 120
        barra_alto = 12
        padding = 6
        line_height = 28
        for tipo, data in sorted(buff_timers.items()):
            restante = data.get("restante", 0)
            duracion = max(0.1, data.get("duracion", 1))
            progreso = max(0.0, min(1.0, restante / duracion))

            # Fondo y borde de barra
            barra_rect = pygame.Rect(x, y, barra_ancho, barra_alto)
            pygame.draw.rect(self.ventana, self.BARRA_FONDO, barra_rect, border_radius=6)
            pygame.draw.rect(self.ventana, self.BARRA_BORDE, barra_rect, width=1, border_radius=6)

            # Relleno proporcional
            fill_rect = barra_rect.copy()
            fill_rect.width = int(barra_ancho * progreso)
            pygame.draw.rect(self.ventana, self.VERDE, fill_rect, border_radius=6)

            # Texto a la derecha
            texto = f"{tipo}: {restante:0.1f}s"
            superficie = self.hud_font.render(texto, True, self.TEXT_COLOR)
            texto_pos = (barra_rect.right + padding, barra_rect.top - 4)
            self.ventana.blit(superficie, texto_pos)

            y += line_height

    def dibujar_jugador(self, jugador, sprite):
        """Dibuja el sprite del jugador en su posicion con efectos de buffo"""
        desplazado = jugador.rect.move(-self.camara_x, 0)

        # Escala visual
        sprite_dibujar = sprite
        dibujar_rect = desplazado
        if jugador.escala_visual != 1.0:
            factor = jugador.escala_visual
            nuevo_ancho = max(1, int(sprite.get_width() * factor))
            nuevo_alto = max(1, int(sprite.get_height() * factor))
            sprite_dibujar = pygame.transform.scale(sprite, (nuevo_ancho, nuevo_alto))
            dibujar_rect = sprite_dibujar.get_rect(center=desplazado.center)

        # Auras (varias capas de color)
        for aura in sorted(jugador.auras, key=lambda a: a.get("size", 0), reverse=True):
            color = aura.get("color")
            size = max(4, aura.get("size", 0))
            if color:
                base_radio = max(dibujar_rect.width, dibujar_rect.height) // 2
                radio = base_radio + size // 2
                pygame.draw.circle(
                    self.ventana,
                    color,
                    dibujar_rect.center,
                    radio,
                    width=max(2, size // 3),
                )

        self.ventana.blit(sprite_dibujar, dibujar_rect)

    def actualizar_pantalla(self):
        """Actualiza la pantalla para mostrar los cambios"""
        pygame.display.flip()

    def get_altura_suelo(self):
        """Retorna la altura del suelo"""
        return self.altura_suelo

    def mover_fondo(self, desplazamiento_x):
        """Mueve el fondo en la direccion especificada

        Args:
            desplazamiento_x: Cantidad de pixeles a mover el fondo (positivo = derecha, negativo = izquierda)
        """
        self.fondo_x += desplazamiento_x

    def set_camara(self, camara_x):
        """Actualiza la posicion de la camara"""
        self.camara_x = camara_x
