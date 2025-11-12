# Juego de Bloques 2048

Un juego estilo 2048 implementado en Python usando Pygame, que demuestra el uso de tres patrones de diseño: **Memento**, **Estrategia** y **Observer**.

## Descripción

Este es un juego de puzzle donde debes colocar bloques con números (2, 4 u 8) en una cuadrícula de 6x7. Cuando colocas un bloque junto a otros bloques del mismo valor, se fusionan multiplicando su valor.

### Mecánica del Juego

- **Colocación**: Haz clic en una columna para colocar un bloque
- **Gravedad**: Los bloques caen hasta encontrar el fondo u otro bloque
- **Fusión**: Cuando un bloque nuevo toca bloques contiguos (arriba, abajo, izquierda, derecha) con el mismo valor:
  - El bloque nuevo multiplica su valor por 2^n (donde n es la cantidad de vecinos iguales)
  - Los bloques viejos se eliminan
  - Las fusiones se evalúan en cadena hasta que no haya más combinaciones posibles

### Ejemplos de Fusión

**1 vecino igual:**
```
Antes:    Después:
  2
  2    →     4
```
Bloque nuevo (2) × 2 = 4

**2 vecinos iguales:**
```
Antes:    Después:
  2
2 2 2  →     8
```
Bloque nuevo (2) × 4 = 8

**3 vecinos iguales:**
```
Antes:    Después:
  2
2 2 2  →    16
  2
```
Bloque nuevo (2) × 8 = 16

## Patrones de Diseño Implementados

### 1. Patrón Memento

**Ubicación**: `juego_bloques.py:50-95`

**Propósito**: Permite deshacer jugadas guardando y restaurando estados previos del juego sin violar el principio de encapsulación.

**Componentes**:
- `Memento`: Guarda el estado de la cuadrícula y el próximo número
- `Caretaker`: Maneja el historial de mementos (máximo 20 estados)
- `Juego`: Actúa como Originator, crea y restaura mementos

**Funcionamiento**:
1. Antes de cada jugada, se guarda el estado actual creando un `Memento`
2. El `Caretaker` mantiene una pila de hasta 20 estados guardados
3. El usuario puede presionar 'Z' o hacer clic en "Deshacer" para restaurar el estado anterior
4. Se restaura tanto la cuadrícula como el próximo número a colocar

**Ventajas**:
- **Encapsulación**: El estado interno del juego está protegido y solo el Juego puede crear/restaurar mementos
- **Historial múltiple**: Se pueden deshacer hasta 20 jugadas consecutivas
- **Bajo acoplamiento**: El Caretaker no conoce ni manipula la estructura interna del estado

**Código relevante**:
```python
# Crear un memento antes de cada jugada
memento = self.crear_memento()
self.caretaker.guardar(memento)

# Deshacer: restaurar el último memento
memento = self.caretaker.deshacer()
self.restaurar_memento(memento)
```

### 2. Patrón Estrategia (Strategy)

**Ubicación**: `juego_bloques.py:98-167`

**Propósito**: Define una familia de algoritmos para calcular el multiplicador de bloques según la cantidad de vecinos iguales, encapsulando cada algoritmo y haciéndolos intercambiables.

**Componentes**:
- `EstrategiaMultiplicacion`: Interfaz abstracta (ABC) que define el contrato para todas las estrategias
- `EstrategiaUnVecino`: Multiplica por 2 cuando hay 1 vecino igual
- `EstrategiaDosVecinos`: Multiplica por 4 cuando hay 2 vecinos iguales
- `EstrategiaTresVecinos`: Multiplica por 8 cuando hay 3 vecinos iguales
- `ContextoMultiplicacion`: Mantiene un diccionario de estrategias y delega el cálculo a la estrategia apropiada

**Funcionamiento**:
1. Cuando un bloque nuevo detecta vecinos con el mismo valor, se cuenta cuántos son
2. El `ContextoMultiplicacion` selecciona la estrategia apropiada según la cantidad de vecinos
3. La estrategia calcula el multiplicador (2, 4 u 8)
4. El valor del bloque nuevo se multiplica por este factor

**Ventajas**:
- **Extensibilidad**: Fácil agregar nuevas estrategias (ej: 4 vecinos = ×16) sin modificar código existente
- **Separación de responsabilidades**: Cada estrategia encapsula su propia lógica
- **Código limpio**: Evita múltiples if/else o switch para determinar el multiplicador
- **Principio Open/Closed**: Abierto a extensión, cerrado a modificación

**Código relevante**:
```python
# El contexto selecciona y aplica la estrategia apropiada
nuevo_bloque.valor = self.contexto_multiplicacion.calcular_nuevo_valor(
    nuevo_bloque.valor,
    len(vecinos_iguales)  # 1, 2 o 3 vecinos
)
```

### 3. Patrón Observer

**Ubicación**: `juego_bloques.py:170-247`

**Propósito**: Define una dependencia uno-a-muchos entre objetos, de modo que cuando un objeto cambia de estado, todos sus dependientes son notificados automáticamente.

**Componentes**:
- `ObserverPatron`: Interfaz abstracta para objetos que observan cambios
- `SubjectPatron`: Clase base que mantiene lista de observers y los notifica
- `Bloque_Observer`: Implementa tanto ObserverPatron como SubjectPatron (es observador y observable)

**Funcionamiento**:
1. Cuando se coloca un bloque nuevo, busca vecinos contiguos con el mismo valor
2. Se establecen relaciones de observación mutua entre el bloque nuevo y sus vecinos iguales
3. El bloque nuevo notifica a sus vecinos, pero marcándose como "nuevo"
4. Los vecinos "viejos" reciben la notificación y se auto-eliminan (simulando la fusión)
5. El valor del bloque nuevo ya fue multiplicado usando el Patrón Estrategia

**Ventajas**:
- **Desacoplamiento**: Los bloques no necesitan conocer la estructura completa del juego
- **Comportamiento diferenciado**: Bloques nuevos y viejos reaccionan de manera distinta a las notificaciones
- **Reactividad**: Los cambios se propagan automáticamente sin coordinación central
- **Extensibilidad**: Fácil agregar nuevos tipos de observers con diferentes comportamientos

**Código relevante**:
```python
# Establecer observación mutua
vecino.agregar_observer(nuevo_bloque)
nuevo_bloque.agregar_observer(vecino)

# El vecino viejo se elimina al recibir notificación
vecino.actualizar(nuevo_bloque, es_nuevo=False)
```

## Requisitos

- Python 3.7+
- Pygame 2.0+

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd Juego2048
```

2. Instala las dependencias:
```bash
pip install pygame
```

O si usas el entorno virtual incluido:
```bash
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

## Cómo Jugar

1. Ejecuta el juego:
```bash
python juego_bloques.py
```

2. **Controles**:
   - **Clic izquierdo**: Colocar bloque en la columna seleccionada
   - **Tecla Z**: Deshacer última jugada
   - **Botón "Deshacer (Z)"**: Deshacer última jugada (esquina superior derecha)

3. **Objetivo**: Crear bloques con el valor más alto posible fusionando bloques estratégicamente

## Estructura del Código

```
juego_bloques.py
├── Patrón Memento (líneas 50-95)
│   ├── Memento                      # Guarda estados del juego (cuadrícula + próximo número)
│   └── Caretaker                    # Maneja historial de hasta 20 estados
│
├── Patrón Estrategia (líneas 98-167)
│   ├── EstrategiaMultiplicacion    # Interfaz abstracta (ABC)
│   ├── EstrategiaUnVecino          # Multiplica por 2 (1 vecino igual)
│   ├── EstrategiaDosVecinos        # Multiplica por 4 (2 vecinos iguales)
│   ├── EstrategiaTresVecinos       # Multiplica por 8 (3 vecinos iguales)
│   └── ContextoMultiplicacion      # Selector de estrategias
│
├── Patrón Observer (líneas 170-247)
│   ├── ObserverPatron              # Interfaz para observers
│   ├── SubjectPatron               # Interfaz para subjects observables
│   └── Bloque_Observer             # Bloque que observa y es observable
│
├── Clase Juego (líneas 249-526)
│   ├── crear_memento()             # Crea snapshot del estado (Patrón Memento)
│   ├── restaurar_memento()         # Restaura estado anterior (Patrón Memento)
│   ├── deshacer_jugada()           # Deshace última jugada
│   ├── colocar_bloque()            # Coloca nuevo bloque y guarda estado
│   ├── configurar_observers()      # Configura relaciones Observer y aplica Estrategia
│   ├── aplicar_gravedad()          # Hace caer los bloques
│   ├── obtener_bloques_contiguos() # Encuentra vecinos adyacentes
│   ├── eliminar_bloque()           # Elimina un bloque de la cuadrícula
│   └── dibujar()                   # Renderiza el juego en pantalla
│
└── main() (líneas 528-575)         # Loop principal del juego
```

## Integración de los Patrones

Los tres patrones trabajan en conjunto durante cada jugada:

```
┌─ Usuario coloca un bloque ─┐
│                             │
▼                             │
1. MEMENTO: Guardar estado    │
   antes de modificar         │
                              │
▼                             │
2. Colocar bloque y aplicar   │
   gravedad                   │
                              │
▼                             │
3. OBSERVER: Detectar vecinos │
   contiguos con mismo valor  │
                              │
▼                             │
4. ESTRATEGIA: Calcular valor │
   nuevo (×2, ×4 o ×8)        │
                              │
▼                             │
5. OBSERVER: Notificar y      │
   eliminar bloques viejos    │
                              │
▼                             │
6. Recursión: Repetir 3-5     │
   si hay más fusiones        │
                              │
▼                             │
Mostrar resultado             │
                              │
[Usuario presiona Deshacer]   │
                              │
MEMENTO: Restaurar estado ────┘
```

**Ejemplo de flujo completo:**
1. Usuario coloca un bloque con valor 2
2. **Memento** guarda el estado actual (antes del cambio)
3. Bloque cae por gravedad y detecta 2 vecinos con valor 2
4. **Estrategia** calcula: 2 × 4 = 8 (EstrategiaDosVecinos)
5. **Observer** notifica a los 2 vecinos viejos, que se auto-eliminan
6. Nuevo bloque (valor 8) detecta 1 vecino con valor 8
7. **Estrategia** calcula: 8 × 2 = 16 (EstrategiaUnVecino)
8. **Observer** elimina el vecino viejo
9. No hay más fusiones posibles, termina recursión
10. Si el usuario presiona deshacer, **Memento** restaura el estado guardado en paso 2

## Características Técnicas

### Fusión en Cadena
El juego evalúa fusiones recursivamente usando los patrones **Observer** y **Estrategia**. Si después de una fusión el bloque resultante tiene más vecinos iguales, se fusiona nuevamente hasta que no haya más combinaciones posibles.

### Vista Previa
El juego muestra el próximo bloque que se colocará, permitiendo planificar la estrategia.

### Indicador Visual de Deshacer
El botón de deshacer cambia de color:
- **Verde**: Hay jugadas para deshacer
- **Gris**: No hay historial disponible

## Configuración

Las constantes del juego se pueden modificar al inicio del archivo:

```python
FILAS = 6              # Altura de la cuadrícula
COLUMNAS = 7           # Ancho de la cuadrícula
TAMANO_CELDA = 80      # Tamaño de cada celda en píxeles
FPS = 60               # Frames por segundo
```

## Colores

Los bloques tienen diferentes colores según su valor:
- **2**: Beige claro (238, 228, 218)
- **4**: Beige oscuro (237, 224, 200)
- **8**: Naranja (242, 177, 121)
- **Valores mayores**: Blanco por defecto

## Autor

Proyecto de demostración de tres patrones de diseño fundamentales: **Memento**, **Estrategia** y **Observer**.

## Licencia

Este proyecto es de código abierto y está disponible para fines educativos.
