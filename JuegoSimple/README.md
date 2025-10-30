## RPG con Patrones de Diseño (Command y Chain of Responsibility) ⚔️

### 👥 Integrantes

- **Bettsy Liliana Garces Buritica** – Código estudiantil: 20231020222 
- **Diego Felipe Barreto Rubiano** – Código estudiantil: 20221020151  
- **Martin Zuluaga Carreño** – Código estudiantil: 20242020252

---

### 🛠️ Tecnología y Enfoque

- **Lenguaje:** Python 🐍
- **Bibliotecas:** `pygame`, `abc`, `typing`, `enum`
- **Principios de Diseño:** Se aplicaron los principios **SOLID** para asegurar un código robusto, fácil de mantener y de extender.

### 📜 Descripción del Proyecto

Este proyecto implementa una batalla de RPG simple, centrada en la aplicación rigurosa de dos patrones de diseño de comportamiento fundamentales para gestionar las acciones del jugador y la validación de estados de manera modular:

#### 1. Patrón Command (Comando)

* **Propósito:** Encapsular una solicitud como un objeto, permitiendo parametrizar clientes con diferentes solicitudes y soportar operaciones de deshacer.
* **Implementación:**
    * Cada acción del juego (Atacar, Defender, Curar) es un **comando concreto** (`AttackCommand`, `DefendCommand`, `HealCommand`) que implementa la interfaz `Command`.
    * El **`GameController`** actúa como invocador, manteniendo un historial de comandos (`command_history`) para la funcionalidad de **Deshacer (`undo()`)**.

#### 2. Patrón Chain of Responsibility (Cadena de Responsabilidad)

* **Propósito:** Evitar acoplar al emisor de una petición con su receptor, dando a más de un objeto la oportunidad de manejar la petición.
* **Implementación:**
    * Se establece una **cadena de manejadores** (`AliveCheckHandler`, `ResourceCheckHandler`, `ExecutionHandler`) para validar y procesar cada comando antes de su ejecución.
    * Esto garantiza que las comprobaciones de estado (como verificar si el personaje está vivo o si tiene recursos) se realicen de manera modular y **extensible** (ejemplificando el Principio Abierto/Cerrado).

---

### ⚙️ Ejecución del Proyecto

El proyecto se ejecuta directamente desde el archivo principal de Python. Asegúrate de tener `pygame` instalado (`pip install pygame`).

```bash
python juego.py
