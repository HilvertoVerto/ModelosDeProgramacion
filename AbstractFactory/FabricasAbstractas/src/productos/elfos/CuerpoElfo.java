package FabricasAbstractas.src.productos.elfos;

import FabricasAbstractas.src.productos.ICuerpo;

public class CuerpoElfo implements ICuerpo {
    @Override
    public String obtenerDescripcion() {
        return "El cuerpo élfico es esbelto y ágil, con sentidos altamente desarrollados. "
        + "Los elfos son longevos y herederos de un linaje mágico ancestral. "
        + "Poseen una conexión profunda con la naturaleza, lo que los hace sigilosos y certeros en combate.";
    }
}
