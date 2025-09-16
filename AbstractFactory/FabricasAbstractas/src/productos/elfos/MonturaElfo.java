package FabricasAbstractas.src.productos.elfos;

import FabricasAbstractas.src.productos.IMontura;

public class MonturaElfo implements IMontura {
    @Override
    public String obtenerDescripcion() {
    return "El ciervo mágico élfico, una criatura noble y veloz, vinculada al bosque encantado. "
     + "Su agilidad y conexión espiritual con su jinete lo convierten en un aliado perfecto "
     + "para incursiones rápidas y combates en terrenos difíciles.";

    }
}
