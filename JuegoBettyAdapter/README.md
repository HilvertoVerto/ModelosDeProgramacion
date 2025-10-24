## JuegoBetty

### 👥 Integrantes

- **Bettsy Liliana Garces Buritica** – Código estudiantil: 20231020222 
- **Diego Felipe Barreto Rubiano** – Código estudiantil: 20221020151  
- **Martin Zuluaga Carreño** – Código estudiantil: 20242020252

---

- **Lenguaje:** Python  
- **Descripción:**  
Este proyecto implementa un juego en el que un personaje obtiene poderes de forma aleatoria, los cuales se representan visualmente en una superficie (surface).

El objetivo principal es demostrar la aplicación del patrón de diseño Decorator, que permite añadir nuevas habilidades o características al personaje sin modificar su estructura base.

Mediante este patrón, cada nuevo poder actúa como una “decoración” que se superpone al personaje existente, ilustrando cómo su comportamiento puede extenderse dinámicamente durante la ejecución del juego.

Adicionalmente, se incorporó el patrón Adapter, encargado de modificar la forma de interacción del jugador. En lugar de utilizar exclusivamente el teclado, ahora es posible controlar al personaje mediante el mouse, lo que demuestra cómo este patrón permite adaptar distintos tipos de entrada de manera flexible y sin alterar el código base.

- **Ejecución:**  
  El proyecto se ejecuta directamente desde el archivo principal:
  ```bash
  python main.py
Diagrama UML
![alt text](image.png)