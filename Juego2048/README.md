# Juego de Bloques 2048

Un juego estilo 2048 implementado en Python usando Pygame, que demuestra el uso de patrones de diseño **Observer** y **Memento**.

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

### 1. Patrón Observer

**Ubicación**: `juego_bloques.py:86-120`

**Propósito**: Permite que los bloques detecten automáticamente cuando tienen vecinos contiguos iguales.

**Componentes**:
- `ObserverPatron`: Interfaz abstracta para objetos que observan cambios
- `SubjectPatron`: Clase base que mantiene y notifica a sus observers
- `Bloque_Observer`: Implementa tanto ObserverPatron como SubjectPatron

**Funcionamiento**:
1. Cuando se coloca un bloque nuevo, detecta vecinos con el mismo valor
2. Se establecen relaciones de observación mutua
3. Los bloques viejos reciben notificación y se auto-eliminan
4. El bloque nuevo se multiplica según la cantidad de vecinos

**Ventajas**:
- Desacoplamiento: Los bloques no necesitan conocer la estructura completa del juego
- Comportamiento diferenciado: Bloques nuevos y viejos reaccionan de manera distinta
- Extensibilidad: Fácil agregar nuevos comportamientos a los bloques

### 2. Patrón Memento

**Ubicación**: `juego_bloques.py:38-83`

**Propósito**: Permite deshacer jugadas guardando y restaurando estados previos del juego.

**Componentes**:
- `Memento`: Guarda el estado de la cuadrícula y el próximo número
- `Caretaker`: Maneja el historial de mementos (máximo 20 estados)
- `Juego`: Crea y restaura mementos

**Funcionamiento**:
1. Antes de cada jugada, se guarda el estado actual
2. El usuario puede presionar 'Z' o hacer clic en "Deshacer"
3. Se restaura el último estado guardado
4. El historial se limita a 20 jugadas para optimizar memoria

**Ventajas**:
- Encapsulación: El estado interno del juego está protegido
- Historial ilimitado: Se pueden deshacer múltiples jugadas
- Sin acoplamiento: El Caretaker no conoce la estructura interna del estado

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
├── Patrón Memento
│   ├── Memento           # Guarda estados del juego
│   └── Caretaker         # Maneja historial de estados
├── Patrón Observer
│   ├── ObserverPatron    # Interfaz para observers
│   ├── SubjectPatron     # Interfaz para subjects
│   └── Bloque_Observer   # Implementa ObserverPatron y SubjectPatron
├── Juego
│   ├── crear_memento()           # Crea snapshot del estado
│   ├── restaurar_memento()       # Restaura estado anterior
│   ├── deshacer_jugada()         # Deshace última jugada
│   ├── colocar_bloque()          # Coloca nuevo bloque
│   ├── configurar_observers()    # Configura relaciones Observer
│   ├── aplicar_gravedad()        # Hace caer los bloques
│   └── dibujar()                 # Renderiza el juego
└── main()                # Loop principal del juego
```

## Características Técnicas

### Fusión en Cadena
El juego evalúa fusiones recursivamente. Si después de una fusión el bloque resultante tiene más vecinos iguales, se fusiona nuevamente hasta que no haya más combinaciones posibles.

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

Proyecto de demostración de patrones de diseño Observer y Memento.

## Licencia

Este proyecto es de código abierto y está disponible para fines educativos.
