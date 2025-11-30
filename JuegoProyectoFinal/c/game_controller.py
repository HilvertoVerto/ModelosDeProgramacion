import pygame
import sys
from m.jugador import Jugador
from v.sprite_loader import SpriteLoader
from v.render import Render
from c.input_handler import InputHandler

class GameController:
    """Controlador principal del juego"""

    def __init__(self, ancho=800, alto=600, fps=60):
        # Inicializar pygame
        pygame.init()

        # Configuración de la ventana
        self.ancho = ancho
        self.alto = alto
        self.fps = fps
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Mario Bros - Demo")

        # Reloj para controlar FPS
        self.reloj = pygame.time.Clock()

        # Inicializar componentes MVC
        self.inicializar_componentes()

        # Estado del juego
        self.corriendo = True

    def inicializar_componentes(self):
        """Inicializa los componentes del patrón MVC"""
        # Vista
        self.render = Render(self.ventana, self.ancho, self.alto)
        self.sprite_loader = SpriteLoader()
        self.sprite_loader.cargar_sprites()

        # Modelo
        self.jugador = Jugador(100, self.alto - 150, self.alto)

        # Controlador
        self.input_handler = InputHandler()

    def manejar_eventos(self):
        """Maneja los eventos del juego usando el InputHandler"""
        # Procesar eventos de cierre
        self.corriendo = self.input_handler.procesar_eventos()

        # Procesar movimiento
        self.input_handler.obtener_movimiento(self.jugador)

    def manejar_salto(self):
        """Maneja el salto del jugador de forma separada para mejor control"""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.jugador.saltar()

    def actualizar(self):
        """Actualiza la lógica del juego"""
        # Actualizar animación del jugador
        self.jugador.actualizar_frame_animacion(self.sprite_loader.get_num_frames())

        # Definir zonas de scroll (20% de cada lado)
        margen_scroll = self.ancho * 0.2
        zona_scroll_izquierda = margen_scroll
        zona_scroll_derecha = self.ancho - margen_scroll

        # Guardar velocidad del jugador antes de aplicar movimiento
        velocidad_jugador = self.jugador.velocidad_x

        # Verificar si debemos mover el fondo en lugar del jugador
        mover_fondo = False

        if velocidad_jugador > 0 and self.jugador.rect.x >= zona_scroll_derecha:
            # Jugador en zona derecha moviéndose a la derecha
            mover_fondo = True
        elif velocidad_jugador < 0 and self.jugador.rect.x <= zona_scroll_izquierda:
            # Jugador en zona izquierda moviéndose a la izquierda
            mover_fondo = True

        # Si debemos mover el fondo, cancelar movimiento del jugador y mover fondo
        if mover_fondo:
            # Mover el fondo en dirección opuesta al movimiento del jugador
            self.render.mover_fondo(velocidad_jugador)
            # Cancelar movimiento horizontal del jugador
            self.jugador.velocidad_x = 0

        # Actualizar física del jugador (incluyendo gravedad y salto)
        self.jugador.update(self.ancho, self.render.get_altura_suelo())

        # Restaurar velocidad para que la animación funcione
        if mover_fondo:
            self.jugador.velocidad_x = velocidad_jugador

    def renderizar(self):
        """Renderiza todos los elementos del juego"""
        # Limpiar pantalla
        self.render.limpiar_pantalla()

        # Dibujar suelo
        self.render.dibujar_suelo()

        # Obtener sprite apropiado del jugador
        sprite_jugador = self.sprite_loader.get_sprite(
            self.jugador.mirando_derecha,
            self.jugador.moviendo,
            self.jugador.frame_actual
        )

        # Dibujar jugador
        self.render.dibujar_jugador(self.jugador.rect, sprite_jugador)

        # Actualizar pantalla
        self.render.actualizar_pantalla()

    def ejecutar(self):
        """Loop principal del juego"""
        while self.corriendo:
            # Manejar eventos e inputs
            self.manejar_eventos()
            self.manejar_salto()

            # Actualizar lógica
            self.actualizar()

            # Renderizar
            self.renderizar()

            # Controlar FPS
            self.reloj.tick(self.fps)

        # Cerrar pygame
        self.cerrar()

    def cerrar(self):
        """Cierra el juego correctamente"""
        pygame.quit()
        sys.exit()
