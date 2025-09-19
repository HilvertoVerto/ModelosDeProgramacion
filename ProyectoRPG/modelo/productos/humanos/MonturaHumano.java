package modelo.productos.humanos;

import modelo.productos.IMontura;

public class MonturaHumano implements IMontura {
    @Override
    public String obtenerDescripcion() {
    return "La montura humana es un caballo de guerra robusto y resistente. "
        + "Criado para la batalla, este caballo combina fuerza y velocidad, "
        + "permitiendo a los jinetes humanos maniobrar con eficacia en el campo de batalla. "
        + "Su entrenamiento riguroso lo hace confiable en situaciones de combate intenso.";
    }
}
