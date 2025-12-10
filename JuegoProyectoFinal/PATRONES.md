# Análisis Detallado de Patrones de Diseño

Este documento proporciona un análisis exhaustivo de cada patrón de diseño implementado en el proyecto, incluyendo su propósito, implementación técnica, flujo de ejecución y justificación.

---

## Tabla de Contenidos

1. [Patrones Comportamentales](#patrones-comportamentales)
   - [State Pattern](#1-state-pattern)
   - [Command Pattern](#2-command-pattern)
   - [Strategy Pattern](#3-strategy-pattern)
   - [Observer Pattern](#4-observer-pattern)
2. [Patrones Estructurales](#patrones-estructurales)
   - [Decorator Pattern](#5-decorator-pattern)
   - [Flyweight Pattern](#6-flyweight-pattern)
3. [Patrones Creacionales](#patrones-creacionales)
   - [Factory Method / Abstract Factory](#7-factory-method--abstract-factory)
4. [Patrones Arquitectónicos](#patrones-arquitectónicos)
   - [MVC](#8-mvc)
   - [Facade Pattern](#9-facade-pattern)

---

## Patrones Comportamentales

### 1. State Pattern

**Propósito:** Permite que un objeto altere su comportamiento cuando su estado interno cambia. El objeto parecerá cambiar de clase.

#### Implementación

**Archivos:** `c/game_state.py`, `c/game_controller.py`

**Estructura:**
```python
# Interfaz base
class GameState:
    def manejar_eventos(self, eventos): ...
    def actualizar(self): ...
    def renderizar(self): ...

# Estados concretos
class MenuState(GameState): ...
class PlayState(GameState): ...
class PauseState(GameState): ...
```

**Contexto (GameController):**
```python
class GameController:
    def __init__(self):
        self.menu_state = factory.crear_menu_state()
        self.play_state = factory.crear_play_state()
        self.pause_state = factory.crear_pause_state(self.play_state)
        self.estado_actual = self.menu_state  # Estado inicial

    def ejecutar(self):
        while self.corriendo:
            # Delega al estado actual (polimorfismo)
            self.estado_actual.manejar_eventos(eventos)
            self.estado_actual.actualizar()
            self.estado_actual.renderizar()
```

#### Flujo de Ejecución

**Ejemplo: Ciclo de vida desde el menú hasta el juego**

1. **Inicio**: `estado_actual = MenuState`
   - `manejar_eventos()`: Detecta ENTER → emite evento `"cambiar_estado"`
   - `actualizar()`: No hace nada
   - `renderizar()`: Dibuja menú principal

2. **Transición**: GameController recibe evento → `estado_actual = PlayState`

3. **Juego**: `estado_actual = PlayState`
   - `manejar_eventos()`: Detecta P → emite evento para pausar
   - `actualizar()`: Actualiza física, enemigos, colisiones
   - `renderizar()`: Dibuja nivel completo

4. **Pausa**: `estado_actual = PauseState`
   - `manejar_eventos()`: Navegación del menú de controles
   - `actualizar()`: No hace nada (juego congelado)
   - `renderizar()`: Dibuja snapshot + overlay

#### Estados Implementados

| Estado | Eventos | Actualización | Renderizado |
|--------|---------|---------------|-------------|
| **MenuState** | ENTER → jugar<br>ESC → salir | Ninguna | Título + opciones |
| **PlayState** | Controles jugador<br>P → pausar<br>ESC → menú | Física, enemigos, colisiones, IA | Nivel, jugador, enemigos, HUD |
| **PauseState** | UP/DOWN → navegar<br>ENTER → cambiar tecla<br>ESC/P → volver | Ninguna | Snapshot + menú controles |

#### Beneficios

✅ **Eliminación de condicionales complejos:** Sin State, necesitarías un `if estado == "menu"` gigante en el loop principal

✅ **Separación de responsabilidades:** Cada estado encapsula su propia lógica

✅ **Facilidad de extensión:** Agregar un nuevo estado (ej. GameOverState) no modifica los existentes

✅ **Código más limpio:** Cada estado es una clase independiente

#### Justificación

**🟢 TOTALMENTE JUSTIFICADO**

- Tres estados con comportamiento radicalmente diferente
- Sin este patrón, el código sería un desastre de `if/elif`
- Facilita agregar nuevos estados sin modificar código existente
- Es el patrón más valioso del proyecto

---

### 2. Command Pattern

**Propósito:** Encapsula una petición como un objeto, permitiendo parametrizar clientes con diferentes peticiones, encolar peticiones y soportar operaciones que se pueden deshacer.

#### Implementación

**Archivos:** `c/commands.py`, `c/input_handler.py`

**Comandos:**
```python
class Command:
    def ejecutar(self, jugador): ...

class MoverIzquierdaCommand(Command):
    def ejecutar(self, jugador):
        jugador.mover_izquierda()

class MoverDerechaCommand(Command):
    def ejecutar(self, jugador):
        jugador.mover_derecha()

class SaltarCommand(Command):
    def ejecutar(self, jugador):
        jugador.saltar()

class DetenerCommand(Command):
    def ejecutar(self, jugador):
        jugador.detener()
```

**InputHandler (Invocador):**
```python
class InputHandler:
    def __init__(self):
        # Comandos
        self.comando_izquierda = MoverIzquierdaCommand()
        self.comando_derecha = MoverDerechaCommand()
        self.comando_salto = SaltarCommand()
        self.comando_detener = DetenerCommand()

        # Mapeo tecla → comando
        self.key_bindings = {
            pygame.K_LEFT: self.comando_izquierda,
            pygame.K_a: self.comando_izquierda,
            pygame.K_RIGHT: self.comando_derecha,
            pygame.K_d: self.comando_derecha,
            pygame.K_SPACE: self.comando_salto,
            # ...
        }

        # Mapeo acción → tecla principal (para UI)
        self.action_keys = {
            "izquierda": pygame.K_LEFT,
            "derecha": pygame.K_RIGHT,
            "saltar": pygame.K_SPACE,
        }
```

#### Flujo de Ejecución

**Ejemplo: Usuario presiona la tecla A**

1. **PlayState.manejar_eventos()** llama a `input_handler.manejar_movimiento(jugador)`

2. **InputHandler** lee las teclas presionadas:
   ```python
   teclas = pygame.key.get_pressed()
   ```

3. **Busca en key_bindings** si alguna tecla presionada tiene un comando asociado:
   ```python
   for tecla, comando in self.key_bindings.items():
       if teclas[tecla] and comando == self.comando_izquierda:
           comando_ejecutado = comando
           break
   ```

4. **Ejecuta el comando**:
   ```python
   comando_ejecutado.ejecutar(jugador)
   # Internamente: jugador.mover_izquierda()
   ```

#### Sistema de Reasignación de Controles

**Cambiar tecla:**
```python
def cambiar_tecla(self, accion, nueva_tecla):
    # 1. Eliminar binding anterior
    tecla_anterior = self.action_keys[accion]
    del self.key_bindings[tecla_anterior]

    # 2. Crear nuevo binding
    self.key_bindings[nueva_tecla] = comando_para_accion
    self.action_keys[accion] = nueva_tecla
```

**Ejemplo concreto:**
- Original: `K_LEFT → comando_izquierda`
- Usuario cambia a `K_j`
- Resultado: `K_j → comando_izquierda` (K_LEFT ya no funciona)

#### Beneficios

✅ **Desacoplamiento:** Separa quién solicita la acción (InputHandler) de quién la ejecuta (Jugador)

✅ **Flexibilidad:** Múltiples teclas pueden ejecutar el mismo comando

✅ **Reasignación dinámica:** Sistema de controles customizables

✅ **Extensibilidad:** Fácil agregar nuevos comandos sin modificar InputHandler

#### Justificación

**🟢 JUSTIFICADO**

- Permite reasignación dinámica de controles (característica implementada en el menú de pausa)
- Mapeo limpio `tecla → comando`
- Sin este patrón, cambiar controles sería muy complicado
- Cumple su propósito de parametrizar acciones

---

### 3. Strategy Pattern

**Propósito:** Define una familia de algoritmos, encapsula cada uno y los hace intercambiables. Strategy permite que el algoritmo varíe independientemente de los clientes que lo usan.

#### Implementación

**Archivos:** `m/estrategias.py`, `m/enemigo.py`

**Estrategias:**
```python
class MovimientoStrategy:
    def mover(self, enemigo): ...
    def puede_atacar(self): ...

class PatrullaPasivaStrategy(MovimientoStrategy):
    def mover(self, enemigo):
        # Movimiento al 40% de velocidad
        velocidad_reducida = enemigo.velocidad_base * 0.4
        enemigo.rect.x += velocidad_reducida * direccion

    def puede_atacar(self):
        return False  # No ataca

class PatrullaAgresivaStrategy(MovimientoStrategy):
    def mover(self, enemigo):
        # Movimiento a velocidad normal
        enemigo.rect.x += enemigo.velocidad_x

    def puede_atacar(self):
        return True  # Sí ataca
```

**Contexto (Enemigo):**
```python
class Enemigo:
    def __init__(self, ...):
        self.estrategia_agresiva = PatrullaAgresivaStrategy()
        self.estrategia_pasiva = PatrullaPasivaStrategy()
        self.estrategia = self.estrategia_pasiva  # Inicial
        self.distancia_agresion = 300  # píxeles

    def actualizar_estrategia(self, posicion_jugador):
        distancia = abs(self.rect.centerx - posicion_jugador[0])
        if distancia <= self.distancia_agresion:
            self.estrategia = self.estrategia_agresiva
        else:
            self.estrategia = self.estrategia_pasiva

    def mover(self):
        self.estrategia.mover(self)  # Delega a la estrategia actual

    def puede_atacar(self):
        return self.estrategia.puede_atacar()
```

#### Flujo de Ejecución

**Ejemplo: Enemigo detecta al jugador**

1. **PlayState.actualizar()** actualiza cada enemigo:
   ```python
   posicion_jugador = (self.jugador.rect.centerx, self.jugador.rect.centery)
   for enemigo in self.enemigos:
       enemigo.update(self.nivel.plataformas, posicion_jugador)
   ```

2. **Enemigo.update()** evalúa la distancia:
   ```python
   def update(self, plataformas, posicion_jugador):
       if posicion_jugador:
           self.actualizar_estrategia(posicion_jugador)
       self.mover()
       # ...
   ```

3. **Cambio dinámico de estrategia:**
   - **Jugador lejos (>300px)**: `estrategia = PatrullaPasivaStrategy`
     - Velocidad: 40% normal
     - Ataca: No

   - **Jugador cerca (≤300px)**: `estrategia = PatrullaAgresivaStrategy`
     - Velocidad: 100% normal
     - Ataca: Sí

4. **PlayState.intentar_disparar()** verifica si puede atacar:
   ```python
   if not enemigo.puede_atacar():
       return  # No dispara si está en estrategia pasiva
   ```

#### Beneficios

✅ **Comportamiento dinámico:** Los enemigos cambian de IA en tiempo real

✅ **Encapsulación:** Cada algoritmo de movimiento está aislado

✅ **Extensibilidad:** Fácil agregar nuevas estrategias (PatrullaCircular, PerseguirJugador, Huir, etc.)

✅ **Código limpio:** Evita `if tipo == "pasivo"` en el código del enemigo

#### Justificación

**🟢 JUSTIFICADO**

- Los enemigos necesitan cambiar comportamiento dinámicamente
- Hace el juego más interesante (enemigos reaccionan al jugador)
- Facilita crear diferentes tipos de IA sin modificar la clase Enemigo
- Cumple perfectamente su propósito

---

### 4. Observer Pattern

**Propósito:** Define una dependencia uno-a-muchos entre objetos, de modo que cuando un objeto cambia de estado, todos sus dependientes son notificados automáticamente.

#### Implementación

**Archivos:** `c/event_bus.py`

**EventBus (Sujeto Observable):**
```python
class EventBus:
    def __init__(self):
        self._suscriptores = {}  # {"evento": [callback1, callback2, ...]}

    def suscribir(self, evento, callback):
        self._suscriptores.setdefault(evento, []).append(callback)

    def emitir(self, evento, payload=None):
        for callback in self._suscriptores.get(evento, []):
            callback(payload)
```

#### Flujo de Ejecución

**Ejemplo: Usuario presiona ENTER en el menú**

1. **Suscripción (Inicialización en GameController):**
   ```python
   self.event_bus.suscribir("cambiar_estado", self.cambiar_estado)
   self.event_bus.suscribir("salir", self._salir)
   self.event_bus.suscribir("game_over", self.game_over)
   self.event_bus.suscribir("victoria", self.victoria)
   ```

2. **Emisión (MenuState detecta tecla):**
   ```python
   if evento.key == pygame.K_RETURN:
       self.event_bus.emitir("cambiar_estado", "juego")
   ```

3. **Notificación (EventBus llama a suscriptores):**
   ```python
   # Busca callbacks registrados para "cambiar_estado"
   for callback in self._suscriptores["cambiar_estado"]:
       callback("juego")  # Llama a self.cambiar_estado("juego")
   ```

4. **Acción (GameController cambia estado):**
   ```python
   def cambiar_estado(self, nuevo_estado):
       if nuevo_estado == "juego":
           self.estado_actual = self.play_state
   ```

#### Eventos Implementados

| Evento | Emisor | Suscriptor | Acción |
|--------|--------|------------|--------|
| `cambiar_estado` | MenuState, PlayState, PauseState | GameController.cambiar_estado | Cambia entre estados |
| `salir` | MenuState | GameController._salir | Cierra el juego |
| `game_over` | PlayState | GameController.game_over | Vuelve al menú |
| `victoria` | PlayState | GameController.victoria | Vuelve al menú |
| `enemigo_eliminado` | PlayState | ⚠️ **NINGUNO** | ⚠️ Evento sin usar |

#### Beneficios

✅ **Desacoplamiento:** Los estados no conocen al GameController directamente

✅ **Flexibilidad:** Fácil agregar nuevos suscriptores sin modificar emisores

✅ **Extensibilidad:** Un evento puede tener múltiples observadores

#### Limitaciones en este Proyecto

⚠️ **Relación 1:1:** Cada evento tiene un solo suscriptor (GameController)

⚠️ **Evento huérfano:** `enemigo_eliminado` se emite pero nadie lo escucha

⚠️ **Simplicidad del proyecto:** La comunicación es predecible y lineal

#### Análisis de Justificación

**🟡 CUESTIONABLE / POSIBLE OVER-ENGINEERING**

**Argumentos a favor:**
- Desacopla estados del GameController
- Facilita agregar sistemas de sonido, logros, partículas, etc.
- Es un buen ejemplo académico del patrón

**Argumentos en contra:**
- Para un proyecto de este tamaño, es innecesario
- Solo hay una relación 1:1:1 (Estado → EventBus → GameController)
- Una referencia directa sería más simple y clara
- No hay múltiples observadores (requisito clave del patrón)

**Alternativa más simple:**
```python
# Sin Observer
class MenuState:
    def __init__(self, game_controller):
        self.controller = game_controller

    def manejar_eventos(self, eventos):
        if evento.key == pygame.K_RETURN:
            self.controller.cambiar_estado("juego")
```

**Conclusión:** El patrón está **correctamente implementado** pero **no es necesario** para la complejidad actual del proyecto. Sería justificable si se agregaran sistemas adicionales que escucharan los mismos eventos (sonidos, logros, estadísticas, efectos visuales, etc.).

---

## Patrones Estructurales

### 5. Decorator Pattern

**Propósito:** Añade responsabilidades a un objeto dinámicamente. Los decoradores proporcionan una alternativa flexible a la herencia para extender funcionalidad.

#### Implementación

**Archivos:** `m/buff_decorators.py`, `m/buff_manager.py`

**Decoradores:**
```python
class BuffDecorator:
    def __init__(self, jugador):
        self.jugador = jugador

    def aplicar(self): ...
    def remover(self): ...

class VelocidadBuff(BuffDecorator):
    def aplicar(self):
        self.jugador.aplicar_multiplicador_velocidad(1.5)

    def remover(self):
        self.jugador.reset_estadisticas()

class SaltoBuff(BuffDecorator):
    def aplicar(self):
        self.jugador.aplicar_impulso_salto(1.4)

    def remover(self):
        self.jugador.reset_estadisticas()

class InvencibleBuff(BuffDecorator):
    def aplicar(self):
        self.jugador.set_invencible(True)
        self.jugador.set_visual(escala=1.2, auras=[...])

    def remover(self):
        self.jugador.set_invencible(False)
        self.jugador.reset_estadisticas()
```

**BuffManager (Gestor de decoradores):**
```python
class BuffManager:
    def __init__(self, buff_classes):
        self.buff_classes = buff_classes  # {"velocidad": VelocidadBuff, ...}
        self.buffos_activos = {}  # {tipo: [(decorator, timestamp), ...]}

    def activar(self, tipo, ahora):
        decorator = self.buff_classes[tipo](jugador)
        self.buffos_activos.setdefault(tipo, []).append((decorator, ahora))
        decorator.aplicar()

    def aplicar(self, jugador, ahora):
        # Remueve buffos expirados
        for tipo, instancias in list(self.buffos_activos.items()):
            instancias_validas = []
            for decorator, timestamp in instancias:
                if ahora - timestamp < DURACION:
                    instancias_validas.append((decorator, timestamp))
                else:
                    decorator.remover()

            if instancias_validas:
                self.buffos_activos[tipo] = instancias_validas
            else:
                del self.buffos_activos[tipo]
```

#### Flujo de Ejecución

**Ejemplo: Jugador recoge buff de velocidad**

1. **Colisión detectada:**
   ```python
   if self.jugador.rect.colliderect(buffo.rect):
       self.buff_manager.activar(buffo.tipo, ahora)
   ```

2. **BuffManager crea decorador:**
   ```python
   decorator = VelocidadBuff(jugador)
   ```

3. **Decorador aplica efecto:**
   ```python
   decorator.aplicar()
   # jugador.velocidad_movimiento = velocidad_base * 1.5
   ```

4. **Jugador ahora se mueve más rápido** (efecto activo)

5. **Después de 5 segundos:**
   ```python
   if ahora - timestamp >= 5000:  # 5 segundos
       decorator.remover()
       # jugador.velocidad_movimiento = velocidad_base
   ```

#### Apilamiento de Buffos

Si el jugador recoge 2 buffos de velocidad:
```python
# Primer buff: velocidad × 1.5
# Segundo buff: velocidad × 1.5 de nuevo = × 2.25 total
```

Los decoradores se pueden **apilar** sin modificar la clase `Jugador`.

#### Beneficios

✅ **Composición sobre herencia:** No necesitas `JugadorRapido`, `JugadorSaltarin`, etc.

✅ **Flexibilidad:** Los efectos se agregan/remueven dinámicamente

✅ **Combinación:** Múltiples buffos pueden estar activos simultáneamente

✅ **Separación de responsabilidades:** La clase `Jugador` no conoce los buffos

#### Justificación

**🟢 JUSTIFICADO**

- Los buffos son efectos temporales que se aplican dinámicamente
- Permite combinar efectos sin modificar `Jugador`
- Es mucho mejor que tener flags booleanos en el jugador
- Facilita agregar nuevos buffos sin tocar código existente

---

### 6. Flyweight Pattern

**Propósito:** Usa compartición para soportar eficientemente gran cantidad de objetos de grano fino.

#### Implementación

**Archivos:** `v/sprite_manager.py`

**SpriteManager (Flyweight Factory):**
```python
class SpriteManager:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._sprites_cargados = {}
        return cls._instancia

    def cargar_sprite(self, nombre, path):
        if nombre not in self._sprites_cargados:
            self._sprites_cargados[nombre] = pygame.image.load(path)
        return self._sprites_cargados[nombre]

    def obtener_sprite(self, nombre):
        return self._sprites_cargados.get(nombre)
```

#### Flujo de Ejecución

**Sin Flyweight (ineficiente):**
```python
# Cada enemigo carga su propia copia del sprite
enemigo1 = Enemigo()
enemigo1.sprite = pygame.image.load("guerrero.png")  # 100 KB

enemigo2 = Enemigo()
enemigo2.sprite = pygame.image.load("guerrero.png")  # Otro 100 KB

# 10 guerreros = 1 MB de memoria
```

**Con Flyweight (eficiente):**
```python
# Carga una sola vez
sprite_manager.cargar_sprite("guerrero", "guerrero.png")  # 100 KB

# Todos comparten la misma instancia
enemigo1.sprite = sprite_manager.obtener_sprite("guerrero")
enemigo2.sprite = sprite_manager.obtener_sprite("guerrero")
# ...
enemigo10.sprite = sprite_manager.obtener_sprite("guerrero")

# 10 guerreros = 100 KB de memoria
```

#### Beneficios

✅ **Ahorro de memoria:** Una sola carga para múltiples instancias

✅ **Rendimiento:** Menos operaciones I/O

✅ **Cache centralizado:** Todas las imágenes en un solo lugar

#### Justificación

**🟢 JUSTIFICADO**

- Múltiples enemigos del mismo tipo comparten sprite
- Ahorra memoria significativamente
- Es un patrón estándar en videojuegos
- Mejora el rendimiento

---

## Patrones Creacionales

### 7. Factory Method / Abstract Factory

**Propósito:** Define una interfaz para crear objetos, pero deja que las subclases decidan qué clase instanciar. Factory Method permite que una clase defiera la instanciación a subclases.

#### Implementación

**Archivos:** `m/enemigo_factory.py`, `m/entidad_factory.py`, `c/state_factory.py`

#### A. EnemigoFactory (Abstract Factory)

```python
class EnemigoFactory:
    @staticmethod
    def crear(tipo, data):
        tipo = (tipo or "").lower()
        if tipo == "arquero":
            return EnemigoFactory._crear_arquero(data)
        if tipo == "mago":
            return EnemigoFactory._crear_mago(data)
        return EnemigoFactory._crear_guerrero(data)

    @staticmethod
    def _crear_guerrero(data):
        return Enemigo(..., arma=Espada())

    @staticmethod
    def _crear_arquero(data):
        return Enemigo(..., arma=Arco())

    @staticmethod
    def _crear_mago(data):
        return Enemigo(..., arma=Baston())
```

**Uso:**
```python
# Carga enemigos desde JSON
enemigos_data = [
    {"tipo": "guerrero", "x": 100, "y": 200},
    {"tipo": "arquero", "x": 300, "y": 200},
    {"tipo": "mago", "x": 500, "y": 200},
]

for data in enemigos_data:
    enemigo = EnemigoFactory.crear(data["tipo"], data)
    enemigos.append(enemigo)
```

**Beneficios:**
- Encapsula la complejidad de crear enemigos con diferentes armas
- Carga desde JSON sin condicionales en el código del juego
- Fácil agregar nuevos tipos sin modificar código existente

**Justificación:** **🟢 JUSTIFICADO**
- Múltiples tipos de enemigos con configuraciones diferentes
- Carga dinámica desde archivos externos
- Simplifica la creación de niveles

---

#### B. StateFactory (Factory Method)

```python
class StateFactory:
    def __init__(self, event_bus, render, sprite_loader, input_handler, jugador, nivel):
        self.event_bus = event_bus
        self.render = render
        # ...

    def crear_menu_state(self):
        return MenuState(self.event_bus, self.render)

    def crear_play_state(self):
        return PlayState(
            self.event_bus,
            self.render,
            self.sprite_loader,
            self.input_handler,
            self.jugador,
            self.nivel,
        )

    def crear_pause_state(self, play_state):
        return PauseState(self.event_bus, self.render, self.input_handler, play_state)
```

**Uso:**
```python
factory = StateFactory(...)
self.menu_state = factory.crear_menu_state()
self.play_state = factory.crear_play_state()
self.pause_state = factory.crear_pause_state(self.play_state)
```

**Análisis de Justificación**

**🟡 CUESTIONABLE / POSIBLE OVER-ENGINEERING**

**Argumentos a favor:**
- Centraliza la creación de estados
- Facilita inyección de dependencias
- Es un buen ejemplo académico del patrón

**Argumentos en contra:**
- Solo se usa **una vez** al inicializar el juego
- Solo crea **3 objetos simples**
- No hay variaciones ni lógica compleja
- Agrega una capa de indirección innecesaria

**Alternativa más simple:**
```python
# En GameController, sin factory
def configurar_estados(self):
    self.menu_state = MenuState(self.event_bus, self.render)
    self.play_state = PlayState(...)
    self.pause_state = PauseState(...)
```

**Conclusión:** El patrón está **correctamente implementado** pero **no aporta valor** para la complejidad actual. Sería útil si:
- Hubieras muchos estados diferentes
- La creación requiriera lógica condicional compleja
- Los estados se crearan dinámicamente en múltiples lugares

---

## Patrones Arquitectónicos

### 8. MVC

**Propósito:** Separa la aplicación en tres componentes interconectados para separar las representaciones internas de la información de las formas en que se presenta y acepta información del usuario.

#### Estructura

```
proyecto/
├── m/  (Model - Modelo)
│   ├── jugador.py       - Entidad jugador con física
│   ├── enemigo.py       - Entidad enemigo con IA
│   ├── nivel.py         - Datos del nivel
│   ├── buff.py          - Datos de buffos
│   └── estrategias.py   - Lógica de IA
│
├── v/  (View - Vista)
│   ├── render.py        - Renderizado de todo
│   ├── sprite_loader.py - Carga de sprites
│   └── sprite_manager.py- Gestión de imágenes
│
└── c/  (Controller - Controlador)
    ├── game_controller.py - Orquestador principal
    ├── game_state.py      - Estados del juego
    ├── input_handler.py   - Manejo de input
    └── commands.py        - Comandos de usuario
```

#### Responsabilidades

**Model (Modelo):**
- Lógica de negocio y datos
- Física del jugador y enemigos
- Algoritmos de IA
- No conoce la vista ni el controlador

**View (Vista):**
- Renderizado de entidades
- Gestión de sprites y gráficos
- Cámara y efectos visuales
- Solo lee datos del modelo, no los modifica

**Controller (Controlador):**
- Orquesta el flujo del juego
- Maneja eventos de usuario
- Actualiza el modelo según input
- Solicita renderizado a la vista

#### Flujo de Datos

```
Usuario presiona tecla
        ↓
Controller (InputHandler) detecta evento
        ↓
Controller ejecuta Command
        ↓
Model (Jugador) actualiza posición
        ↓
Controller solicita renderizado
        ↓
View (Render) dibuja el jugador en nueva posición
        ↓
Pantalla actualizada
```

#### Beneficios

✅ **Separación de responsabilidades:** Cada capa tiene un propósito claro

✅ **Mantenibilidad:** Cambios en una capa no afectan otras

✅ **Testabilidad:** Puedes probar la lógica sin GUI

✅ **Reutilización:** El modelo puede usarse con diferentes vistas

#### Justificación

**🟢 TOTALMENTE JUSTIFICADO**

- Es el patrón arquitectónico base del proyecto
- Estructura clara y mantenible
- Facilita el desarrollo en equipo
- Estándar en desarrollo de videojuegos

---

### 9. Facade Pattern

**Propósito:** Proporciona una interfaz unificada a un conjunto de interfaces en un subsistema. Facade define una interfaz de alto nivel que hace que el subsistema sea más fácil de usar.

#### Implementación

**Archivo:** `c/game_controller.py`

**GameController (Facade):**
```python
class GameController:
    def __init__(self, ancho=800, alto=600, fps=60):
        # Inicializa todos los subsistemas
        pygame.init()
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()

        # Carga nivel
        self.nivel_actual = Nivel.desde_archivo("niveles/nivel1.json")

        # Crea componentes
        self.render = Render(...)
        self.sprite_loader = SpriteLoader()
        self.jugador = Jugador(...)
        self.input_handler = InputHandler()

        # Configura estados
        self.configurar_estados()

    def ejecutar(self):
        """Interfaz simple para el cliente"""
        while self.corriendo:
            eventos = pygame.event.get()
            self.estado_actual.manejar_eventos(eventos)
            self.estado_actual.actualizar()
            self.estado_actual.renderizar()
            self.reloj.tick(self.fps)
```

**Cliente (main.py):**
```python
# Sin facade necesitarías inicializar todo manualmente
# Con facade, solo:
if __name__ == "__main__":
    juego = GameController()
    juego.ejecutar()
```

#### Beneficios

✅ **Simplicidad:** El cliente solo necesita 2 líneas de código

✅ **Ocultación de complejidad:** Todo el setup está encapsulado

✅ **Interfaz unificada:** Un solo punto de entrada al sistema

✅ **Desacoplamiento:** El cliente no depende de componentes internos

#### Justificación

**🟢 TOTALMENTE JUSTIFICADO**

- Simplifica enormemente el punto de entrada
- Oculta la complejidad de inicialización
- Es esencial para que `main.py` sea tan simple
- Facilita crear múltiples instancias del juego si fuera necesario

---

## Resumen de Justificación

| Patrón | Justificación | Notas |
|--------|---------------|-------|
| **State** | 🟢 Totalmente justificado | El más valioso del proyecto |
| **Command** | 🟢 Justificado | Permite controles remapeables |
| **Strategy** | 🟢 Justificado | IA dinámica de enemigos |
| **Observer** | 🟡 Cuestionable | **Posible over-engineering** para este tamaño de proyecto |
| **Decorator** | 🟢 Justificado | Sistema de buffos flexible |
| **Flyweight** | 🟢 Justificado | Ahorra memoria significativamente |
| **Factory (Enemies)** | 🟢 Justificado | Carga enemigos desde JSON |
| **Factory (States)** | 🟡 Cuestionable | **Posible over-engineering**, usado solo una vez |
| **MVC** | 🟢 Totalmente justificado | Arquitectura base del proyecto |
| **Facade** | 🟢 Totalmente justificado | Simplifica entrada al sistema |

---

## Conclusión

El proyecto demuestra una implementación **técnicamente correcta** de múltiples patrones de diseño. La mayoría están **bien justificados** y aportan valor real al código. Sin embargo:

### Patrones con Posible Over-Engineering

**1. Observer Pattern (EventBus)**
- **Problema:** Relación 1:1:1 simple, no aprovecha la naturaleza "uno-a-muchos" del patrón
- **Mejora sugerida:** Agregar sistemas que escuchen eventos (sonidos, logros, partículas) o simplificar con referencias directas

**2. StateFactory**
- **Problema:** Solo crea 3 objetos una vez, no aporta valor
- **Mejora sugerida:** Crear estados directamente en GameController sin factory

### Recomendaciones

Para un **proyecto académico**, estos patrones están excelentes como **ejemplos de aprendizaje**. Para **producción real**, considera:

- ✅ Mantener: State, Command, Strategy, Decorator, Flyweight, MVC, Facade, EnemigoFactory
- 🟡 Revisar: Observer (expandir uso o simplificar), StateFactory (eliminar o justificar)

El código demuestra buen conocimiento de patrones de diseño, con implementaciones limpias y correctas. Las áreas de mejora identificadas son oportunidades de refinamiento, no errores.
