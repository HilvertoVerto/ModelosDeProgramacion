
# 📘 Modelos de Programación – Repositorio de Proyectos

Este repositorio reúne los proyectos desarrollados durante la clase de **Modelos de Programación**, mostrando la aplicación práctica de distintos patrones de diseño y paradigmas de programación.

---

## 👥 Integrantes
- **Bettsy Liliana Garces Buritica** – Código estudiantil: 20231020222 
- **Diego Felipe Barreto Rubiano** – Código estudiantil: 20221020151  
- **Martin Zuluaga Carreño** – Código estudiantil: 20242020252

---

## 📂 Proyectos

### 1️⃣ Calculadora
- **Lenguaje:** C++  
- **Descripción:**  
  Implementación de una calculadora que permite realizar operaciones en diferentes sistemas numéricos: **binario, octal y decimal**.  
- **Estado:** Proyecto inicial del curso.  

---

### 2️⃣ Abstract Factory
- **Lenguaje:** Java  
- **Descripción:**  
  Este proyecto implementa un **sistema de creación de personajes para un juego de fantasía**, utilizando patrones de diseño de software para lograr una arquitectura **flexible y extensible**.  

  El programa permite a los usuarios **seleccionar una raza** y, a partir de ella, **generar diferentes partes del personaje** (cuerpo, arma, armadura, etc.) de manera consistente.  

  El objetivo principal es demostrar la aplicación de los patrones **Singleton** y **Abstract Factory** para mantener la coherencia de los personajes y evitar la creación de objetos de **razas mixtas**.  
- **Estado:** Proyecto intermedio.  

---

### 3️⃣ Proyecto RPG
## Nota sobre la rama principal de desarrollo

El estado más actualizado y en desarrollo activo de este proyecto se encuentra en la rama **`reorganizacion`**.  
Para acceder al código más reciente, se recomienda trabajar sobre dicha rama en lugar de `main`.

- **Lenguaje:** Java (Web con Apache Tomcat)  
- **Descripción:**  
  Extiende el trabajo realizado en *Abstract Factory*, incorporando una **interfaz gráfica web** y añadiendo la implementación de nuevos patrones de diseño como **Object Pool** y **Singleton**.  

  El sistema se despliega en un entorno web, facilitando la interacción con los personajes creados y mostrando la escalabilidad de la arquitectura.  
- **Requisitos:**
  - **JDK OpenJDK 17.0.16** o superior  
  - **Apache Tomcat 11.0.11**  
- **Ejecución:**
  1. Iniciar el servidor Tomcat.  
  2. Copiar el archivo `ProyectoRPG.war` en la carpeta `webapps` de Tomcat.  
  3. Acceder desde el navegador a:  
     ```
     http://localhost:8080/ProyectoRPG
     ```  
- **Estado:** Proyecto avanzado con despliegue en entorno web.  

---

## 4. Explicación del proyecto

## Nota sobre la rama principal de desarrollo

El estado más actualizado y en desarrollo activo de este proyecto se encuentra en la rama **`reorganizacion`**.
Este proyecto es un ejemplo de cómo aplicar el **patrón de diseño Composite** en Java dentro de un escenario musical.  
Se define una interfaz `Musical` con operaciones comunes (`tocar`, `afinar`, `crear`, `eliminar`).  
A partir de ella:  
- La clase **Banda** funciona como un objeto compuesto, capaz de contener varios elementos musicales (instrumentos o incluso otras bandas).  
- La clase **Instrumento** es un objeto simple que solo puede tocar y afinar.  
- Se crean tres tipos de instrumentos (`Guitarra`, `Tambor`, `Flauta`), con tres ejemplos inventados de cada uno.  

---

El programa permite agrupar instrumentos en una banda, afinarlos y tocarlos, mostrando todo el proceso por consola.
## 📝 Notas
Este repositorio se actualizará con los avances de la materia, integrando nuevos patrones de diseño, prácticas y mejoras en cada proyecto.
