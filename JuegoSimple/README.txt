# ⚔️ RPG Táctico con Patrones de Diseño

## Implementación de Patrones Command y Chain of Responsibility

Este proyecto es una simulación simple de un juego de rol (RPG) por turnos en Python con Pygame. El objetivo principal es la aplicación rigurosa de los patrones de diseño **Command** y **Chain of Responsibility**, buscando una alta adherencia a los principios **SOLID**.

---

## 🏗️ Arquitectura y Principios de Diseño

La estructura del código busca el **desacoplamiento** total entre acciones, validaciones y la interfaz.

### 1. Patrón Command: Encapsulación de Acciones

El patrón Command permite la creación de un sistema de historial y la funcionalidad de **deshacer (Undo)**.

- **Command (Interfaz):** Define la interfaz común para todas las acciones (`execute()` y `undo()`). (Principio de Segregación de Interfaces).
- **Comandos Concretos:** Clases como `AttackCommand`, `DefendCommand` y `HealCommand` que encapsulan una acción, sus datos y la lógica para revertirla. (Principio de Responsabilidad Única - SRP).
- **GameController:** Actúa como el **Invocador**. Almacena la historia de comandos.

### 2. Patrón Chain of Responsibility: Gestión de Validaciones

Este patrón desacopla las validaciones de la lógica de negocio, haciendo el sistema fácilmente extensible.

- **Handler (Interfaz):** Define la estructura de la cadena (`handle()`) y el método para enlazar al siguiente handler (`set_next()`).
- **Handlers Concretos:**
    - **AliveCheckHandler:** Verifica si los personajes involucrados están vivos.
    - **ResourceCheckHandler:** Verifica precondiciones como tener pociones o no estar al máximo de HP.
    - **ExecutionHandler:** El último eslabón; ejecuta el comando si todas las validaciones previas pasaron.
- **Ventaja de Diseño:** La Cadena se puede extender para añadir nuevas reglas de validación sin modificar los handlers existentes o el controlador. (Principio Abierto/Cerrado - OCP).

### 3. Principios SOLID Adicionales

- **Inversión de Dependencias (DIP):** El `GameController` depende de las abstracciones (`Command` y `Handler`), no de sus implementaciones concretas.
- **Responsabilidad Única (SRP):** `GameView` se encarga solo de la UI, separada de la lógica de juego.

---

## 🚀 Puesta en Marcha

### Requisitos

El proyecto requiere la librería `pygame`.

    pip install pygame

### Ejecución

1.  Guarde el código fuente como `rpg_patterns.py`.
2.  Ejecute el archivo desde la línea de comandos:

    python rpg_patterns.py

---

## 🎮 Controles de Juego

Las acciones del jugador se mapean directamente a la ejecución de un objeto Command.

- **Q - AttackCommand:** Inflige daño al enemigo.
- **W - DefendCommand:** Otorga una bonificación de defensa temporal.
- **E - HealCommand:** Restaura HP, consume 1 poción. Validado por la Cadena de Responsabilidad.
- **R - Deshacer:** Revierte el efecto de la última acción del jugador, utilizando la capacidad de `undo()` del patrón Command.
