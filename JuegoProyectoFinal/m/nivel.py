import json
import os
import pygame


class Nivel:
    """Datos de un nivel: plataformas solidas, punto de spawn y recursos."""

    def __init__(
        self,
        nombre,
        plataformas,
        spawn,
        altura_suelo,
        fondo=None,
        tile_size=64,
        ancho_mundo=1600,
        enemigos=None,
        buffos=None,
        meta_x=None,
    ):
        self.nombre = nombre
        self.plataformas = plataformas
        self.spawn = spawn
        self.altura_suelo = altura_suelo
        self.fondo = fondo
        self.tile_size = tile_size
        self.ancho_mundo = ancho_mundo
        self.enemigos = enemigos or []
        self.buffos = buffos or []
        self.meta_x = meta_x or ancho_mundo

    @classmethod
    def desde_archivo(cls, ruta, ancho_ventana=800, alto_ventana=600):
        """
        Carga un nivel desde un archivo JSON.
        Si no hay plataformas definidas, genera un suelo por defecto.
        """
        with open(ruta, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        tile_size = data.get("tile_size", 64)
        altura_suelo = data.get("altura_suelo", tile_size)
        spawn_data = data.get("spawn", {"x": 100, "y": alto_ventana - (2 * tile_size)})
        plataformas_data = data.get("plataformas", [])
        fondo = data.get("fondo")
        nombre = data.get("nombre", os.path.splitext(os.path.basename(ruta))[0])
        enemigos = data.get("enemigos", [])
        ancho_mundo = data.get("ancho_mundo")
        buffos = data.get("buffos", [])
        meta_x = data.get("meta_x")

        plataformas = cls._crear_plataformas(plataformas_data)

        if not plataformas:
            # Suelo por defecto del ancho del mundo
            plataformas.append(
                pygame.Rect(0, alto_ventana - altura_suelo, ancho_ventana * 2, altura_suelo)
            )

        # Calcular ancho del mundo si no se definio
        if ancho_mundo is None:
            max_plat = max((p.right for p in plataformas), default=ancho_ventana)
            ancho_mundo = max(ancho_ventana, max_plat + tile_size)

        return cls(
            nombre=nombre,
            plataformas=plataformas,
            spawn=(spawn_data["x"], spawn_data["y"]),
            altura_suelo=altura_suelo,
            fondo=fondo,
            tile_size=tile_size,
            ancho_mundo=ancho_mundo,
            enemigos=enemigos,
            buffos=buffos,
            meta_x=meta_x,
        )

    @staticmethod
    def _crear_plataformas(plataformas_data):
        """Convierte estructuras simples en pygame.Rect"""
        plataformas = []
        for plataforma in plataformas_data:
            try:
                plataformas.append(
                    pygame.Rect(
                        plataforma["x"],
                        plataforma["y"],
                        plataforma["w"],
                        plataforma["h"],
                    )
                )
            except KeyError:
                continue
        return plataformas
