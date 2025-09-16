package FabricasAbstractas.src.fabricas;

import FabricasAbstractas.src.productos.*;
import FabricasAbstractas.src.productos.orcos.*;

public class FabricaOrcos extends FabricaAbstracta {
    private static FabricaOrcos instancia;

    private FabricaOrcos() {}

    public static FabricaOrcos getInstancia() {
        if (instancia == null) {
            instancia = new FabricaOrcos();
        }
        return instancia;
    }

    @Override
    public ICuerpo crearCuerpo() {
        return new CuerpoOrco();
    }

    @Override
    public IMontura crearMontura() {
        return new MonturaOrco();
    }

    @Override
    public IArma crearArma() {
        return new ArmaOrco();
    }

    @Override
    public IArmadura crearArmadura() {
        return new ArmaduraOrco();
    }
}
