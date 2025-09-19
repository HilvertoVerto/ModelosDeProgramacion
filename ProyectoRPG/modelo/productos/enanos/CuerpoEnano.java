package modelo.productos.enanos;

import modelo.productos.ICuerpo;

public class CuerpoEnano implements ICuerpo {
    @Override
    public String obtenerDescripcion() {
    return "El cuerpo humano pertenece a una civilización versátil y equilibrada. "
        + "Los humanos no destacan en fuerza ni en agilidad, pero poseen una gran adaptabilidad. "
        + "Son resistentes a largas batallas y tienen la capacidad de aprender diversas técnicas, "
        + "lo que los convierte en soldados confiables en cualquier ejército.";

    }
}
