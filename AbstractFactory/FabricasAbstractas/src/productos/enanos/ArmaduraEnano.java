package FabricasAbstractas.src.productos.enanos;

import FabricasAbstractas.src.productos.IArmadura;

public class ArmaduraEnano implements IArmadura {
    @Override
    public String obtenerDescripcion() {
    return "La armadura de un enano es robusta y resistente, diseñada para soportar los rigores de la batalla en las montañas.";  
    }
}
