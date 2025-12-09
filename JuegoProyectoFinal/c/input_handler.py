import pygame
from c.commands import (
    Command,
    DetenerCommand,
    MoverDerechaCommand,
    MoverIzquierdaCommand,
    SaltarCommand,
)


class InputHandler:
    """Clase encargada de manejar las entradas del usuario usando el patron Command.

    Implementacion correcta del patron Command:
    - key_bindings: mapea cada tecla individual a su comando
    - action_keys: mapea cada accion a su tecla principal (para UI)
    """

    def __init__(self):
        # Comandos (patron Command)
        self.comando_izquierda: Command = MoverIzquierdaCommand()
        self.comando_derecha: Command = MoverDerechaCommand()
        self.comando_detener: Command = DetenerCommand()
        self.comando_salto: Command = SaltarCommand()

        # Mapeo de teclas a comandos (tecla -> comando)
        self.key_bindings = {
            pygame.K_LEFT: self.comando_izquierda,
            pygame.K_a: self.comando_izquierda,
            pygame.K_RIGHT: self.comando_derecha,
            pygame.K_d: self.comando_derecha,
            pygame.K_SPACE: self.comando_salto,
            pygame.K_UP: self.comando_salto,
            pygame.K_w: self.comando_salto,
        }

        # Mapeo de acciones a tecla principal (para mostrar en UI)
        self.action_keys = {
            "izquierda": pygame.K_LEFT,
            "derecha": pygame.K_RIGHT,
            "saltar": pygame.K_SPACE,
        }

    def cambiar_tecla(self, accion, nueva_tecla):
        """Cambia la tecla asignada a una accion (patron Command correcto).

        1. Encuentra el comando asociado a la accion
        2. Elimina el binding anterior de esa accion
        3. Agrega el nuevo binding
        4. Actualiza action_keys
        """
        if accion not in self.action_keys:
            return

        # Obtener el comando para esta accion
        comando_map = {
            "izquierda": self.comando_izquierda,
            "derecha": self.comando_derecha,
            "saltar": self.comando_salto,
        }
        comando = comando_map.get(accion)
        if not comando:
            return

        # Eliminar binding anterior de esta accion
        tecla_anterior = self.action_keys[accion]
        if tecla_anterior in self.key_bindings:
            del self.key_bindings[tecla_anterior]

        # Agregar nuevo binding
        self.key_bindings[nueva_tecla] = comando
        self.action_keys[accion] = nueva_tecla

    def agregar_tecla(self, accion, nueva_tecla):
        """Agrega una tecla adicional a una accion."""
        comando_map = {
            "izquierda": self.comando_izquierda,
            "derecha": self.comando_derecha,
            "saltar": self.comando_salto,
        }
        comando = comando_map.get(accion)
        if comando and nueva_tecla not in self.key_bindings:
            self.key_bindings[nueva_tecla] = comando

    def remover_tecla(self, accion, tecla):
        """Remueve una tecla de una accion."""
        if tecla in self.key_bindings:
            del self.key_bindings[tecla]
            # Si era la tecla principal, asignar otra
            if self.action_keys.get(accion) == tecla:
                # Buscar otra tecla para esta accion
                comando_map = {
                    "izquierda": self.comando_izquierda,
                    "derecha": self.comando_derecha,
                    "saltar": self.comando_salto,
                }
                comando = comando_map.get(accion)
                for k, v in self.key_bindings.items():
                    if v == comando:
                        self.action_keys[accion] = k
                        break

    def obtener_teclas(self, accion):
        """Obtiene las teclas asignadas a una accion."""
        comando_map = {
            "izquierda": self.comando_izquierda,
            "derecha": self.comando_derecha,
            "saltar": self.comando_salto,
        }
        comando = comando_map.get(accion)
        if not comando:
            return []

        # Devolver todas las teclas que mapean a este comando
        teclas = [k for k, v in self.key_bindings.items() if v == comando]
        return teclas

    def procesar_eventos(self):
        """Procesa eventos de salida de la app."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return False
        return True

    def manejar_movimiento(self, jugador):
        """Ejecuta comandos de movimiento segun teclas presionadas (patron Command correcto)."""
        teclas = pygame.key.get_pressed()

        # Verificar cada tecla presionada y ejecutar su comando asociado
        comando_ejecutado = None
        for tecla, comando in self.key_bindings.items():
            if teclas[tecla]:
                if comando in (self.comando_izquierda, self.comando_derecha):
                    comando_ejecutado = comando
                    break

        if comando_ejecutado:
            comando_ejecutado.ejecutar(jugador)
        else:
            self.comando_detener.ejecutar(jugador)

    def manejar_salto(self, jugador):
        """Ejecuta comando de salto si corresponde (patron Command correcto)."""
        teclas = pygame.key.get_pressed()

        # Verificar cada tecla presionada y ejecutar su comando asociado
        for tecla, comando in self.key_bindings.items():
            if teclas[tecla] and comando == self.comando_salto:
                comando.ejecutar(jugador)
                break
