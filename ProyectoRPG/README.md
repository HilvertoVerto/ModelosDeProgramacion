### 📘 ProyectoRPG

---

## 👥 Integrantes
- **Bettsy Liliana Garces Buritica** – Código estudiantil: 20231020222 
- **Diego Felipe Barreto Rubiano** – Código estudiantil: 20221020151  
- **Martin Zuluaga Carreño** – Código estudiantil: 20242020252


## Nota sobre la rama principal de desarrollo

El estado más actualizado y en desarrollo activo de este proyecto se encuentra en la rama **`reorganizacion`**.  
Para acceder al código más reciente, se recomienda trabajar sobre dicha rama en lugar de `main`.

- **Lenguaje:** Java (Web con Apache Tomcat)  
- **Descripción:**  
  Este proyecto implementa un **sistema de creación de personajes para un juego de fantasía**, utilizando patrones de diseño de software para lograr una arquitectura **flexible y extensible**.  

  El programa permite a los usuarios **seleccionar una raza** y, a partir de ella, **generar diferentes partes del personaje** (cuerpo, arma, armadura, etc.) de manera consistente.  

  El objetivo principal es demostrar la aplicación de los patrones **Abstract Factory**, **Singleton** y **Object Pool**, asegurando la **coherencia en la creación de personajes** y evitando combinaciones incoherentes entre razas o tipos de objetos.  

  Además, el sistema cuenta con una **interfaz gráfica web**, desplegada sobre **Apache Tomcat**, que facilita la interacción del usuario con los personajes creados y permite observar la **escalabilidad y modularidad** de la arquitectura.  
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
