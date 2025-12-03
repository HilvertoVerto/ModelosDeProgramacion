import pygame
import os


class SpriteManager:
    """Gestor centralizado de sprites del juego (Flyweight pattern)."""

    def __init__(self):
        self.sprites = {}
        self.base_path = "graficos"

    def cargar_todos(self):
        """Carga todos los sprites del juego."""
        self._cargar_jugador()
        self._cargar_enemigos()
        self._cargar_proyectiles()
        self._cargar_buffos()

    def _cargar_jugador(self):
        """Carga el sprite del jugador."""
        path = os.path.join(self.base_path, "Sprites", "Jugador.png")
        if os.path.exists(path):
            sprite = pygame.image.load(path).convert_alpha()
            # Escalar a tamaño apropiado
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites["jugador"] = sprite
            self.sprites["jugador_izq"] = pygame.transform.flip(sprite, True, False)
        else:
            # Fallback: círculo blanco
            superficie = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(superficie, (255, 255, 255), (32, 32), 32)
            self.sprites["jugador"] = superficie
            self.sprites["jugador_izq"] = superficie

    def _cargar_enemigos(self):
        """Carga sprites de enemigos."""
        enemigos = [
            ("Enemigo_1_.png", "enemigo_guerrero"),
            ("Enemigo_2_.png", "enemigo_arquero"),
            ("Enemigo_3_.png", "enemigo_mago"),
            ("Enemigo_4_.png", "enemigo_extra"),
        ]

        for archivo, nombre in enemigos:
            path = os.path.join(self.base_path, "Sprites", archivo)
            if os.path.exists(path):
                sprite = pygame.image.load(path).convert_alpha()
                # Escalar a tamaño apropiado (48x48 para enemigos)
                sprite = pygame.transform.scale(sprite, (48, 48))
                self.sprites[nombre] = sprite
            else:
                # Fallback: rectángulo de color
                superficie = pygame.Surface((48, 48), pygame.SRCALPHA)
                pygame.draw.rect(superficie, (200, 60, 60), (0, 0, 48, 48), border_radius=8)
                self.sprites[nombre] = superficie

        # Si no hay sprites específicos, usar el primero para todos
        if "enemigo_guerrero" in self.sprites:
            if "enemigo_arquero" not in self.sprites:
                self.sprites["enemigo_arquero"] = self.sprites["enemigo_guerrero"]
            if "enemigo_mago" not in self.sprites:
                self.sprites["enemigo_mago"] = self.sprites["enemigo_guerrero"]

    def _cargar_proyectiles(self):
        """Carga sprite de proyectiles."""
        path = os.path.join(self.base_path, "Sprites", "Proyectil.png")
        if os.path.exists(path):
            sprite = pygame.image.load(path).convert_alpha()
            # Escalar pequeño para proyectiles
            sprite = pygame.transform.scale(sprite, (24, 16))
            self.sprites["proyectil"] = sprite
            self.sprites["proyectil_izq"] = pygame.transform.flip(sprite, True, False)
        else:
            # Fallback: rectángulo amarillo
            superficie = pygame.Surface((12, 6), pygame.SRCALPHA)
            pygame.draw.rect(superficie, (255, 200, 50), (0, 0, 12, 6), border_radius=3)
            self.sprites["proyectil"] = superficie
            self.sprites["proyectil_izq"] = superficie

    def _cargar_buffos(self):
        """Carga sprites de buffs."""
        # Cargar sprites individuales para cada tipo de buff
        buffs = [
            ("Bufo_1_.png", "buff_velocidad"),
            ("Bufo_2_.png", "buff_salto"),
            ("Bufo_3_.png", "buff_invencible"),
        ]

        for archivo, nombre in buffs:
            path = os.path.join(self.base_path, "Sprites", archivo)
            if os.path.exists(path):
                sprite = pygame.image.load(path).convert_alpha()
                # Escalar a tamaño apropiado (32x32 para buffs)
                sprite = pygame.transform.scale(sprite, (32, 32))
                self.sprites[nombre] = sprite
            else:
                # Fallback: círculo de color
                superficie = pygame.Surface((32, 32), pygame.SRCALPHA)
                color = (255, 215, 0)  # Amarillo por defecto
                if "invencible" in nombre:
                    color = (60, 179, 113)
                elif "salto" in nombre:
                    color = (70, 130, 180)
                pygame.draw.circle(superficie, color, (16, 16), 16)
                self.sprites[nombre] = superficie

    def get_sprite(self, nombre):
        """Obtiene un sprite por nombre."""
        return self.sprites.get(nombre)

    def get_sprite_jugador(self, mirando_derecha):
        """Obtiene el sprite del jugador según su dirección."""
        if mirando_derecha:
            return self.sprites.get("jugador")
        else:
            return self.sprites.get("jugador_izq")

    def get_sprite_enemigo(self, tipo_arma):
        """Obtiene el sprite del enemigo según su tipo de arma."""
        tipo_map = {
            "Espada": "enemigo_guerrero",
            "Arco": "enemigo_arquero",
            "Baston": "enemigo_mago",
        }
        nombre = tipo_map.get(tipo_arma, "enemigo_guerrero")
        return self.sprites.get(nombre, self.sprites.get("enemigo_guerrero"))

    def get_sprite_proyectil(self, direccion):
        """Obtiene el sprite del proyectil según su dirección."""
        if direccion > 0:
            return self.sprites.get("proyectil")
        else:
            return self.sprites.get("proyectil_izq")

    def get_sprite_buff(self, tipo):
        """Obtiene el sprite del buff según su tipo."""
        nombre = f"buff_{tipo}"
        return self.sprites.get(nombre, self.sprites.get("buff_velocidad"))
