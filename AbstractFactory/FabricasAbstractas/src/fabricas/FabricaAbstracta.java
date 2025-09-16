package FabricasAbstractas.src.fabricas;

import FabricasAbstractas.src.productos.*;

public abstract class FabricaAbstracta {
    public abstract ICuerpo crearCuerpo();
    public abstract IMontura crearMontura();
    public abstract IArma crearArma();
    public abstract IArmadura crearArmadura();
}
