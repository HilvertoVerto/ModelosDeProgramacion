import pygame

class Jugador(pygame.sprite.Sprite):
    """Clase que representa al jugador del juego"""

    def __init__(self, x, y, alto_ventana):
        super().__init__()

        # Configuración de física
        self.GRAVEDAD = 0.8
        self.VELOCIDAD_SALTO = -15
        self.VELOCIDAD_MOVIMIENTO = 5

        # Posición y dimensiones
        self.rect = pygame.Rect(x, y, 64, 64)
        self.alto_ventana = alto_ventana

        # Física
        self.velocidad_y = 0
        self.velocidad_x = 0
        self.en_suelo = False

        # Estado del jugador
        self.mirando_derecha = True
        self.moviendo = False

        # Animación
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 5

    def aplicar_gravedad(self):
        """Aplica la gravedad al jugador"""
        self.velocidad_y += self.GRAVEDAD
        self.rect.y += self.velocidad_y

    def verificar_colision_suelo(self, altura_suelo):
        """Verifica si el jugador está en el suelo"""
        if self.rect.bottom >= self.alto_ventana - altura_suelo:
            self.rect.bottom = self.alto_ventana - altura_suelo
            self.velocidad_y = 0
            self.en_suelo = True
        else:
            self.en_suelo = False

    def aplicar_movimiento_horizontal(self):
        """Aplica el movimiento horizontal"""
        self.rect.x += self.velocidad_x

    def limitar_bordes(self, ancho_ventana):
        """Limita el movimiento a los bordes de la ventana"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho_ventana:
            self.rect.right = ancho_ventana

    def mover_izquierda(self):
        """Establece el movimiento hacia la izquierda"""
        self.velocidad_x = -self.VELOCIDAD_MOVIMIENTO
        self.mirando_derecha = False
        self.moviendo = True

    def mover_derecha(self):
        """Establece el movimiento hacia la derecha"""
        self.velocidad_x = self.VELOCIDAD_MOVIMIENTO
        self.mirando_derecha = True
        self.moviendo = True

    def detener(self):
        """Detiene el movimiento horizontal"""
        self.velocidad_x = 0
        self.moviendo = False

    def saltar(self):
        """Hace que el jugador salte si está en el suelo"""
        if self.en_suelo:
            self.velocidad_y = self.VELOCIDAD_SALTO
            self.en_suelo = False

    def actualizar_frame_animacion(self, num_frames):
        """Actualiza el frame de animación"""
        if self.moviendo and num_frames > 0:
            self.contador_animacion += 1
            if self.contador_animacion >= self.velocidad_animacion:
                self.contador_animacion = 0
                self.frame_actual = (self.frame_actual + 1) % num_frames
        else:
            self.frame_actual = 0

    def update(self, ancho_ventana, altura_suelo):
        """Actualiza el estado del jugador"""
        self.aplicar_gravedad()
        self.verificar_colision_suelo(altura_suelo)
        self.aplicar_movimiento_horizontal()
        self.limitar_bordes(ancho_ventana)
