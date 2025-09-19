package modelo.productos.humanos;

import modelo.productos.ICuerpo;

public class CuerpoHumano implements ICuerpo {
    @Override
    public String obtenerDescripcion() {
    return "El cuerpo humano pertenece a una civilización versátil y equilibrada. "
        + "Los humanos no destacan en fuerza ni en agilidad, pero poseen una gran adaptabilidad. "
        + "Son resistentes a largas batallas y tienen la capacidad de aprender diversas técnicas, "
        + "lo que los convierte en soldados confiables en cualquier ejército.";

    }
}
