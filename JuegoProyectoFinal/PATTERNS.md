# Patrones de diseño en el proyecto

- **MVC**  
  - Carpetas `m/`, `v/`, `c/` separan modelo, vista y controlador.
  - `main.py` inicia `GameController` como orquestador.

- **State**  
  - `c/game_state.py`: `GameState` (Estado base), `MenuState`, `PlayState`.  
  - `c/state_factory.py` crea los estados y `GameController` conmuta entre ellos.

- **Observer (Publish/Subscribe)**  
  - `c/event_bus.py`: `EventBus` permite suscripción/emisión de eventos (`game_over`, `victoria`, etc.).

- **Command**  
  - `c/commands.py`: comandos de entrada (`MoverIzquierdaCommand`, `MoverDerechaCommand`, `SaltarCommand`, `DetenerCommand`).  
  - `c/input_handler.py` mapea teclas a comandos y los ejecuta sobre el jugador.

- **Factory Method**  
  - `m/nivel.py: Nivel.desde_archivo()` crea niveles desde JSON.  
  - `m/entidad_factory.py` instancia enemigos (vía `EnemigoFactory`) y buffos desde datos.  
  - `c/state_factory.py` fabrica estados del juego.

- **Abstract Factory**  
  - `m/enemigo_factory.py` crea enemigos de distintos tipos con su arma (`Espada`, `Arco`, `Baston`) configurando color/estrategia.

- **Strategy**  
  - `m/estrategias.py`: `MovimientoStrategy` y `PatrullaStrategy`.  
  - `m/enemigo.py` delega su movimiento horizontal a una estrategia.

- **Decorator**  
  - `m/buff_decorators.py`: `VelocidadBuff`, `SaltoBuff`, `InvencibleBuff` decoran al jugador sumando efectos y visuales por stack (aura y tinte).  
  - `m/buff_manager.py` administra activacion/expiracion y aplica decoradores al jugador.

- **Scheduler/Timer (Time-based control)**  
  - `m/buff_manager.py` controla expiracion y tiempo restante de buffos (reincidiendo reinicia el timer), expone datos para el HUD.

- **Template Method (simple)**  
  - `GameState` define la interfaz `manejar_eventos/actualizar/renderizar` que los estados concretos implementan.

- **Game Loop**  
  - `c/game_controller.py: GameController.ejecutar` implementa el ciclo típico de juegos (eventos → update → render → tick).

- **Facade (ligero)**  
  - `GameController` expone un único punto de entrada que orquesta input, estados, render y modelo; `main.py` solo crea/ejecuta esta fachada.

- **Flyweight (recursos)**  
  - `v/sprite_loader.py` carga y reutiliza superficies de sprites, evitando duplicados al compartir las mismas instancias en memoria.
