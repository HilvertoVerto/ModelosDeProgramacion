import pygame


class Jugador(pygame.sprite.Sprite):
    """Clase que representa al jugador del juego"""

    def __init__(self, x, y, alto_ventana):
        super().__init__()

        # Configuracion de fisica
        self.GRAVEDAD = 0.8
        self.velocidad_salto_base = -15
        self.velocidad_movimiento_base = 5
        self.velocidad_salto = self.velocidad_salto_base
        self.velocidad_movimiento = self.velocidad_movimiento_base

        # Posicion y dimensiones
        self.rect = pygame.Rect(x, y, 64, 64)
        self.alto_ventana = alto_ventana

        # Fisica
        self.velocidad_y = 0
        self.velocidad_x = 0
        self.en_suelo = False
        self.invencible = False

        # Estado del jugador
        self.mirando_derecha = True
        self.moviendo = False

        # Animacion
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 5
        # Visual
        self.escala_visual = 1.0
        self.auras = []  # lista de {"color": (r,g,b), "size": px}

    def aplicar_gravedad(self):
        """Aplica la gravedad al jugador"""
        self.velocidad_y += self.GRAVEDAD
        self.rect.y += self.velocidad_y

    def aplicar_movimiento_horizontal(self):
        """Aplica el movimiento horizontal"""
        self.rect.x += self.velocidad_x

    def limitar_bordes(self, ancho_mundo):
        """Limita el movimiento a los bordes del mundo"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho_mundo:
            self.rect.right = ancho_mundo

    def mover_izquierda(self):
        """Establece el movimiento hacia la izquierda"""
        self.velocidad_x = -self.velocidad_movimiento
        self.mirando_derecha = False
        self.moviendo = True

    def mover_derecha(self):
        """Establece el movimiento hacia la derecha"""
        self.velocidad_x = self.velocidad_movimiento
        self.mirando_derecha = True
        self.moviendo = True

    def detener(self):
        """Detiene el movimiento horizontal"""
        self.velocidad_x = 0
        self.moviendo = False

    def saltar(self):
        """Hace que el jugador salte si esta en el suelo"""
        if self.en_suelo:
            self.velocidad_y = self.velocidad_salto
            self.en_suelo = False

    def actualizar_frame_animacion(self, num_frames):
        """Actualiza el frame de animacion"""
        if self.moviendo and num_frames > 0:
            self.contador_animacion += 1
            if self.contador_animacion >= self.velocidad_animacion:
                self.contador_animacion = 0
                self.frame_actual = (self.frame_actual + 1) % num_frames
        else:
            self.frame_actual = 0

    def resolver_colisiones_horizontal(self, plataformas):
        """Resuelve colisiones horizontales contra las plataformas"""
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.left
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.right
                self.velocidad_x = 0

    def resolver_colisiones_vertical(self, plataformas):
        """Resuelve colisiones verticales y determina si esta en el suelo"""
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.top
                    self.en_suelo = True
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.bottom
                self.velocidad_y = 0

    def update(self, ancho_mundo, plataformas):
        """Actualiza el estado del jugador con colisiones"""
        self.en_suelo = False

        # Movimiento horizontal y colision lateral
        self.aplicar_movimiento_horizontal()
        self.resolver_colisiones_horizontal(plataformas)

        # Movimiento vertical y colision con plataformas/suelo
        self.aplicar_gravedad()
        self.resolver_colisiones_vertical(plataformas)

        self.limitar_bordes(ancho_mundo)

    # Buffos y estados
    def aplicar_multiplicador_velocidad(self, factor):
        self.velocidad_movimiento = self.velocidad_movimiento_base * factor

    def aplicar_impulso_salto(self, factor):
        self.velocidad_salto = self.velocidad_salto_base * factor

    def reset_estadisticas(self):
        self.velocidad_movimiento = self.velocidad_movimiento_base
        self.velocidad_salto = self.velocidad_salto_base
        self.invencible = False
        self.escala_visual = 1.0
        self.auras = []

    def set_invencible(self, valor):
        self.invencible = valor

    def set_visual(self, escala=1.0, auras=None):
        """Actualiza la apariencia visual (solo render, no colision)."""
        self.escala_visual = escala
        self.auras = auras or []
