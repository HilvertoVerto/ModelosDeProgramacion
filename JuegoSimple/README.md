## RPG con Patrones de Diseño (Command y Chain of Responsibility) ⚔️

### 👥 Integrantes

- **Bettsy Liliana Garces Buritica** – Código estudiantil: 20231020222 
- **Diego Felipe Barreto Rubiano** – Código estudiantil: 20221020151  
- **Martin Zuluaga Carreño** – Código estudiantil: 20242020252

---

- **Lenguaje:** Python 🐍
- **Bibliotecas:** `pygame`, `abc`, `typing`, `enum`
- **Descripción:** Este proyecto implementa una batalla de RPG simple, centrada en la aplicación rigurosa de dos patrones de diseño clave para manejar las acciones del jugador y la validación de estados:

1.  **Patrón Command (Comando):**
    * Cada acción del juego (Atacar, Defender, Curar) se encapsula como un objeto de comando (`AttackCommand`, `DefendCommand`, `HealCommand`).
    * Esto permite **desacoplar** la acción de quien la ejecuta y de quien la invoca, logrando que el `GameController` pueda gestionar y almacenar comandos fácilmente.
    * Se incluye una función `undo()` en cada comando, lo que implementa la capacidad de **Deshacer** la última acción, una característica poderosa de este patrón.

2.  **Patrón Chain of Responsibility (Cadena de Responsabilidad):**
    * Se establece una cadena de manejadores (`AliveCheckHandler`, `ResourceCheckHandler`, `ExecutionHandler`) para validar y procesar cada comando antes de su ejecución.
    * Esto garantiza que las comprobaciones de estado (como verificar si el personaje está vivo o si tiene pociones) se realicen de manera modular y **extensible** (Principio Abierto/Cerrado).

El diseño sigue los principios **SOLID** para asegurar un código robusto, fácil de mantener y de extender.

- **Ejecución:** El proyecto se ejecuta directamente desde el archivo principal:

```bash
python main.py
