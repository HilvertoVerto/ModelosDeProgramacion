# Demo estilo Mario (MVC + patrones)

Juego de plataformas basico en Pygame siguiendo Modelo-Vista-Controlador y varios patrones de diseno.

## Controles
- **Flechas / A-D**: mover izquierda-derecha
- **W / Flecha arriba / Espacio**: saltar
- **P**: pausar y configurar controles
- **ESC**: salir al menú (o volver del menú de pausa)

## Características actuales
- Cámara que sigue al jugador y fondo con parallax; jugador con sprite personalizado (Shrek)
- **Sprites visuales**: Jugador, enemigos (3 tipos diferentes), proyectiles y buffos con imágenes únicas
- **Enemigos inteligentes** (3 tipos: guerrero/arquero/mago):
  - Cada uno con arma y sprite diferente
  - **IA dinámica con Strategy**: Cambian entre comportamiento pasivo (lejos del jugador) y agresivo (cerca del jugador)
  - Velocidad reducida y sin ataques cuando están lejos
  - Velocidad normal y atacan cuando detectan al jugador
- **Mecánica de pisar enemigos**: Salta sobre los enemigos para eliminarlos (estilo Mario Bros)
  - El jugador rebota automáticamente al pisar un enemigo
  - Contacto lateral sin invencibilidad mata al jugador
- **Sistema de controles remapeable** (Patrón Command):
  - Presiona **P** para pausar y acceder al menú de configuración
  - Cambia las teclas de cada acción (mover, saltar)
  - Las teclas antiguas se desactivan al reasignar
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

## Patrones de Diseño Implementados

### Patrones Comportamentales

#### 1. **State Pattern** (Máquina de Estados)
- **Dónde**: `c/game_state.py`, `c/game_controller.py`
- **Qué hace**: Permite que el juego cambie su comportamiento según el estado actual
- **Estados**: MenuState, PlayState, PauseState
- **Beneficio**: Cada estado tiene su propia lógica de eventos, actualización y renderizado

#### 2. **Command Pattern** (Comandos)
- **Dónde**: `c/commands.py`, `c/input_handler.py`
- **Qué hace**: Encapsula acciones del jugador como objetos (MoverIzquierda, MoverDerecha, Saltar)
- **Implementación**: Sistema de mapeo `tecla → comando` con reasignación dinámica
- **Beneficio**: Permite cambiar controles en tiempo de ejecución desde el menú de pausa

#### 3. **Strategy Pattern** (Estrategias de IA)
- **Dónde**: `m/estrategias.py`, `m/enemigo.py`
- **Qué hace**: Define diferentes algoritmos de movimiento para enemigos
- **Estrategias**: PatrullaPasiva (lento, no ataca) y PatrullaAgresiva (normal, ataca)
- **Beneficio**: Los enemigos cambian su comportamiento dinámicamente según la distancia al jugador

#### 4. **Observer Pattern** (Observador)
- **Dónde**: `c/event_bus.py`
- **Qué hace**: Sistema de eventos para comunicación desacoplada entre componentes
- **Eventos**: `cambiar_estado`, `game_over`, `victoria`, `salir`
- **Beneficio**: Los estados emiten eventos sin conocer quién los escucha
- **Nota**: Ver `PATRONES.md` para análisis de justificación

### Patrones Estructurales

#### 5. **Decorator Pattern** (Decoradores)
- **Dónde**: `m/buff_decorators.py`, `m/buff_manager.py`
- **Qué hace**: Añade efectos temporales al jugador (velocidad, salto, invencibilidad)
- **Beneficio**: Los buffos se pueden apilar y combinar sin modificar la clase Jugador

#### 6. **Flyweight Pattern** (Peso Ligero)
- **Dónde**: `v/sprite_manager.py`
- **Qué hace**: Comparte sprites entre múltiples entidades para ahorrar memoria
- **Beneficio**: Carga una vez las imágenes y las reutiliza en todos los enemigos del mismo tipo

### Patrones Creacionales

#### 7. **Factory Method / Abstract Factory** (Fábricas)
- **Dónde**: `m/enemigo_factory.py`, `m/entidad_factory.py`, `c/state_factory.py`
- **Qué hace**: Crea objetos complejos sin exponer la lógica de construcción
- **EnemigoFactory**: Crea enemigos de diferentes tipos (guerrero/arquero/mago) con sus armas
- **StateFactory**: Crea los estados del juego
- **Nota**: Ver `PATRONES.md` para análisis de justificación

### Patrones Arquitectónicos

#### 8. **MVC (Model-View-Controller)**
- **Model** (`m/`): Lógica de juego, entidades, física
- **View** (`v/`): Renderizado, sprites, cámara
- **Controller** (`c/`): Manejo de eventos, estados, input

#### 9. **Facade Pattern** (Fachada)
- **Dónde**: `c/game_controller.py`
- **Qué hace**: Simplifica la interfaz del sistema de juego
- **Beneficio**: `main.py` solo necesita crear el GameController y llamar `ejecutar()`

---

**Para análisis detallado de cada patrón, ver `PATRONES.md`**

## Ejecutar
```bash
pip install pygame
python main.py
```
