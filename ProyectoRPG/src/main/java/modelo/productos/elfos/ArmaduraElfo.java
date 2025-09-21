package modelo.productos.elfos;

import modelo.productos.IArmadura;

public class ArmaduraElfo implements IArmadura {
    @Override
    public String obtenerDescripcion() {
    return "La armadura élfica está hecha de metales livianos y encantados. "
     + "Permite gran movilidad y combina protección con elegancia. "
     + "Brilla con un leve resplandor mágico que desvía ataques menores, "
     + "y sus detalles reflejan la tradición milenaria de los clanes élficos.";

    }
}
