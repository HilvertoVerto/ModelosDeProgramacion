import os
import sys
import pygame
from m.jugador import Jugador
from m.nivel import Nivel
from v.sprite_loader import SpriteLoader
from v.render import Render
from c.input_handler import InputHandler
from c.event_bus import EventBus
from c.state_factory import StateFactory


class GameController:
    """Controlador principal del juego con maquina de estados"""

    def __init__(self, ancho=800, alto=600, fps=60):
        pygame.init()

        # Configuracion de la ventana
        self.ancho = ancho
        self.alto = alto
        self.fps = fps
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Mario Bros - Demo")

        # Reloj para controlar FPS
        self.reloj = pygame.time.Clock()

        # Bus de eventos y estado
        self.event_bus = EventBus()
        self.corriendo = True
        self.estado_actual = None

        # Cargar datos y objetos principales
        self.cargar_nivel_principal()
        self.inicializar_componentes()
        self.configurar_estados()

    def cargar_nivel_principal(self):
        """Carga el nivel base desde datos externos"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        proyecto_dir = os.path.dirname(base_dir)
        nivel_path = os.path.join(proyecto_dir, "niveles", "nivel1.json")
        self.nivel_actual = Nivel.desde_archivo(nivel_path, ancho_ventana=self.ancho, alto_ventana=self.alto)

    def inicializar_componentes(self):
        """Inicializa componentes del patron MVC"""
        self.render = Render(
            self.ventana,
            self.ancho,
            self.alto,
            altura_suelo=self.nivel_actual.altura_suelo,
            fondo=self.nivel_actual.fondo,
        )
        self.sprite_loader = SpriteLoader()
        self.sprite_loader.cargar_sprites()

        spawn_x, spawn_y = self.nivel_actual.spawn
        self.jugador = Jugador(spawn_x, spawn_y, self.alto)

        # Controlador de entrada
        self.input_handler = InputHandler()

    def configurar_estados(self):
        """Configura la maquina de estados simple"""
        factory = StateFactory(
            self.event_bus,
            self.render,
            self.sprite_loader,
            self.input_handler,
            self.jugador,
            self.nivel_actual,
        )

        self.menu_state = factory.crear_menu_state()
        self.play_state = factory.crear_play_state()
        self.pause_state = factory.crear_pause_state(self.play_state)

        self.estado_actual = self.menu_state
        self.event_bus.suscribir("cambiar_estado", self.cambiar_estado)
        self.event_bus.suscribir("salir", self._salir)
        self.event_bus.suscribir("game_over", self.game_over)
        self.event_bus.suscribir("victoria", self.victoria)

    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado actual si es valido"""
        if nuevo_estado == "menu":
            self.estado_actual = self.menu_state
            self.render.set_camara(0)
        elif nuevo_estado == "juego":
            if self.estado_actual == self.menu_state:
                self.play_state.reset()
            self.estado_actual = self.play_state
        elif nuevo_estado == "pausa":
            self.pause_state.capturar_snapshot()
            self.estado_actual = self.pause_state

    def game_over(self, _payload=None):
        """Regresa al menu al perder"""
        self.cambiar_estado("menu")

    def victoria(self, _payload=None):
        """Regresa al menu al ganar"""
        self.cambiar_estado("menu")

    def _salir(self, _payload=None):
        self.corriendo = False

    def ejecutar(self):
        """Loop principal del juego"""
        while self.corriendo:
            eventos = pygame.event.get()

            # Eventos globales
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.corriendo = False

            # Delegar en el estado actual
            self.estado_actual.manejar_eventos(eventos)
            self.estado_actual.actualizar()
            self.estado_actual.renderizar()

            self.reloj.tick(self.fps)

        self.cerrar()

    def cerrar(self):
        """Cierra el juego correctamente"""
        pygame.quit()
        sys.exit()
