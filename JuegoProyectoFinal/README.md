# Juego tipo Mario Bros - Demo

Juego de plataformas básico desarrollado con Pygame siguiendo el patrón de diseño MVC (Modelo-Vista-Controlador).

## Características

- Movimiento lateral del personaje (izquierda/derecha)
- Sistema de salto con física realista
- Animación de sprites durante el movimiento
- Gravedad y colisiones con el suelo

## Controles

- **Flechas IZQUIERDA/DERECHA** o **A/D**: Mover el personaje
- **ESPACIO**, **W** o **FLECHA ARRIBA**: Saltar
- **ESC**: Salir del juego

## Estructura del Proyecto (MVC)

```
.
├── main.py                 # Archivo principal para ejecutar el juego
├── m/                      # MODELO - Lógica del juego y entidades
│   ├── __init__.py
│   └── jugador.py         # Clase del jugador (física, estado, movimiento)
├── v/                      # VISTA - Renderizado y sprites
│   ├── __init__.py
│   ├── sprite_loader.py   # Cargador de sprites del personaje
│   └── render.py          # Renderizador del juego
├── c/                      # CONTROLADOR - Control del juego
│   ├── __init__.py
│   ├── game_controller.py # Controlador principal del juego
│   └── input_handler.py   # Manejador de inputs del usuario
└── Sprites/               # Recursos gráficos
    └── traje/             # Sprites del personaje
        ├── frente0/
        ├── frente1/
        ├── frente2/
        └── frente3/
```

## Requisitos

- Python 3.x
- Pygame

## Instalación

```bash
pip install pygame
```

## Ejecución

```bash
python main.py
```

## Arquitectura MVC

### Modelo (m/)
Contiene la lógica del juego y las entidades:
- **jugador.py**: Maneja la física, movimiento, saltos y estado del jugador

### Vista (v/)
Maneja todo lo relacionado con la visualización:
- **sprite_loader.py**: Carga y gestiona los sprites del personaje
- **render.py**: Renderiza los elementos del juego en pantalla

### Controlador (c/)
Coordina el modelo y la vista:
- **game_controller.py**: Loop principal del juego, coordina actualización y renderizado
- **input_handler.py**: Procesa las entradas del usuario

## Próximas características

- [ ] Enemigos
- [ ] Plataformas
- [ ] Sistema de puntuación
- [ ] Niveles
- [ ] Power-ups
- [ ] Sonido y música
