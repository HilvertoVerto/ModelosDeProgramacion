package FabricasAbstractas.src.fabricas;

import FabricasAbstractas.src.productos.*;
import FabricasAbstractas.src.productos.enanos.*;

public class FabricaEnanos extends FabricaAbstracta {
    private static FabricaEnanos instancia;

    private FabricaEnanos() {}

    public static FabricaEnanos getInstancia() {
        if (instancia == null) {
            instancia = new FabricaEnanos();
        }
        return instancia;
    }

    @Override
    public ICuerpo crearCuerpo() {
        return new CuerpoEnano();
    }

    @Override
    public IMontura crearMontura() {
        return new MonturaEnano();
    }

    @Override
    public IArma crearArma() {
        return new ArmaEnano();
    }

    @Override
    public IArmadura crearArmadura() {
        return new ArmaduraEnano();
    }
}
