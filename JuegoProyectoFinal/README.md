# Demo estilo Mario (MVC + patrones)

Juego de plataformas basico en Pygame siguiendo Modelo-Vista-Controlador y varios patrones de diseno.

## Controles
- Flechas / A-D: mover izquierda-derecha
- W / Flecha arriba / Espacio: saltar
- ESC: salir al menu

## Caracteristicas actuales
- Camara que sigue al jugador y fondo con parallax; jugador dibujado como circulo con auras por buffos
- Enemigos que patrullan (3 tipos: guerrero/arquero/mago) cada uno con arma y color; arma visible junto a ellos; contacto sin invencible mata
- Buffos velocidad/salto/invencible con stacks, aura creciente y temporizador con barra en HUD; el mismo tipo reinicia tiempo
- Pozos que causan derrota y meta al final del mapa para ganar
- Nivel cargado desde JSON (`niveles/nivel1.json`)

## Archivos principales (que hace cada uno)
- `main.py`: punto de entrada; instancia `GameController` y ejecuta el loop.
- `c/game_controller.py`: fachada/orquestador; bucle de juego, eventos globales, cambio de estado, suscripcion a eventos de game over/victoria.
- `c/game_state.py`: estados `MenuState` y `PlayState`; aplica decoradores de buffos, controla camara, derrota/victoria y HUD de barras de tiempo.
- `c/input_handler.py` + `c/commands.py`: maneja entradas usando Command (mover/saltar/detener).
- `c/event_bus.py`: Observer simple para eventos (`game_over`, `victoria`, etc.).
- `c/state_factory.py`: crea los estados del juego (Factory).
- `m/jugador.py`: fisicas del jugador, salto/movimiento/colisiones y auras visuales.
- `m/enemigo.py`: enemigo con estrategia de movimiento y arma (color segun arma).
- `m/armas.py`: define armas (Espada, Arco, Baston) con dano/alcance/color, cooldown y proyectiles.
- `m/proyectil.py`: proyectil disparado por armas a distancia.
- `m/buff_manager.py`: administra activacion, expiracion y efectos de buffos (Decorator + timers).
- `m/estrategias.py`: Strategy de movimiento (patrulla).
- `m/buff.py`: datos de buffo; `m/buff_decorators.py`: Decorator para efectos acumulables.
- `m/nivel.py`: carga nivel desde JSON (Factory Method), guarda plataformas, spawn, meta y buffos.
- `m/entidad_factory.py` + `m/enemigo_factory.py`: crean enemigos de distintos tipos (guerrero/arquero/mago) con armas y buffos desde datos (Abstract Factory/Factory Method).
- `v/render.py`: dibuja fondo/camara, plataformas, enemigos, jugador con auras, meta y HUD de barras de buffos.
- `v/sprite_loader.py`: carga sprites y genera fallback circular para el jugador.
- `niveles/nivel1.json`: nivel demo con plataformas, buffos y enemigos tipados.
- `PATTERNS.md`: resumen de patrones aplicados (State, Observer, Command, Strategy, Decorator, Factory Method/Abstract Factory, Game Loop, Facade, Flyweight, Timers).

## Patrones usados
Ver `PATTERNS.md` para detalle por clase.

## Ejecutar
```bash
pip install pygame
python main.py
```
