package FabricasAbstractas.src.productos.orcos;

import FabricasAbstractas.src.productos.IArma;

public class ArmaOrco implements IArma {
    @Override
    public String obtenerDescripcion() {
    return "El hacha de guerra orca, tosca pero devastadora. "
     + "Hecha de hierro pesado y adornada con runas de guerra. "
     + "Cada golpe puede destrozar armaduras y escudos con facilidad. "
     + "Es un arma temida por su brutalidad.";
    }
}
