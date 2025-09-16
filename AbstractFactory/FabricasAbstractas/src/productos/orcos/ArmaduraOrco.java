package FabricasAbstractas.src.productos.orcos;

import FabricasAbstractas.src.productos.IArmadura;

public class ArmaduraOrco implements IArmadura {
    @Override
    public String obtenerDescripcion() {
    return "La armadura orca está compuesta de placas de hierro burdo y pieles endurecidas. "
     + "Su diseño no busca estética, sino intimidación y supervivencia. "
     + "Ofrece gran protección contra ataques cuerpo a cuerpo, aunque sacrifica movilidad.";
    }
}
