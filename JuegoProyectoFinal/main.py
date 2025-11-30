#!/usr/bin/env python3
"""
Juego tipo Mario Bros - Demo
Autor: Sistema MVC
Descripción: Juego de plataformas básico con movimiento lateral y salto

Controles:
- Flechas IZQUIERDA/DERECHA o A/D: Mover el personaje
- ESPACIO, W o FLECHA ARRIBA: Saltar
- ESC: Salir del juego
"""

from c.game_controller import GameController

def main():
    """Función principal del juego"""
    # Crear y ejecutar el juego
    juego = GameController(ancho=800, alto=600, fps=60)
    juego.ejecutar()

if __name__ == "__main__":
    main()
