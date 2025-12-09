# Demo estilo Mario (MVC + patrones)

Juego de plataformas basico en Pygame siguiendo Modelo-Vista-Controlador y varios patrones de diseno.

## Controles
- Flechas / A-D: mover izquierda-derecha
- W / Flecha arriba / Espacio: saltar
- ESC: salir al menu

## Caracteristicas actuales
- Camara que sigue al jugador y fondo con parallax; jugador con sprite personalizado (Shrek)
- **Sprites visuales**: Jugador, enemigos (3 tipos diferentes), proyectiles y buffos con imágenes únicas
- Enemigos que patrullan (3 tipos: guerrero/arquero/mago) cada uno con arma y sprite diferente
- **Mecánica de pisar enemigos**: Salta sobre los enemigos para eliminarlos (estilo Mario Bros)
  - El jugador rebota automáticamente al pisar un enemigo
  - Usa patrón Observer para emitir evento `"enemigo_eliminado"`
  - Contacto lateral sin invencibilidad mata al jugador
- Buffos velocidad/salto/invencible con sprites únicos, stacks, aura creciente y temporizador con barra en HUD
- Pozos que causan derrota y meta al final del mapa para ganar
- Nivel cargado desde JSON (`niveles/nivel1.json`)

## Archivos principales (que hace cada uno)
- `main.py`: punto de entrada; instancia `GameController` y ejecuta el loop.
- `c/game_controller.py`: fachada/orquestador; bucle de juego, eventos globales, cambio de estado, suscripcion a eventos de game over/victoria.
- `c/game_state.py`: estados `MenuState` y `PlayState`; aplica decoradores de buffos, controla camara, **mecánica de pisar enemigos**, derrota/victoria y HUD de barras de tiempo.
- `c/input_handler.py` + `c/commands.py`: maneja entradas usando Command (mover/saltar/detener).
- `c/event_bus.py`: Observer simple para eventos (`game_over`, `victoria`, `enemigo_eliminado`, etc.).
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
- `v/render.py`: dibuja fondo/camara, plataformas, enemigos con sprites, jugador con auras, proyectiles, buffos, meta y HUD de barras de buffos.
- `v/sprite_loader.py`: carga sprite del jugador (Shrek).
- `v/sprite_manager.py`: gestor centralizado de sprites (Flyweight); carga jugador, enemigos, proyectiles y buffos.
- `niveles/nivel1.json`: nivel demo con plataformas, buffos y enemigos tipados.
- `PATTERNS.md`: resumen de patrones aplicados (State, Observer, Command, Strategy, Decorator, Factory Method/Abstract Factory, Game Loop, Facade, Flyweight, Timers).
- `DIAGRAMA_UML.md`: diagrama de clases completo en formato Mermaid con todas las relaciones y patrones.

## Patrones usados
Ver `PATTERNS.md` para detalle por clase.

## Ejecutar
```bash
pip install pygame
python main.py
```
