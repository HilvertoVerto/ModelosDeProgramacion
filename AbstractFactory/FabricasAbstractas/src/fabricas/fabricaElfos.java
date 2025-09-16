package FabricasAbstractas.src.fabricas;

import FabricasAbstractas.src.productos.*;
import FabricasAbstractas.src.productos.elfos.*;

public class FabricaElfos extends FabricaAbstracta {
    private static FabricaElfos instancia;

    private FabricaElfos() {}

    public static FabricaElfos getInstancia() {
        if (instancia == null) {
            instancia = new FabricaElfos();
        }
        return instancia;
    }

    @Override
    public ICuerpo crearCuerpo() {
        return new CuerpoElfo();
    }

    @Override
    public IMontura crearMontura() {
        return new MonturaElfo();
    }

    @Override
    public IArma crearArma() {
        return new ArmaElfo();
    }

    @Override
    public IArmadura crearArmadura() {
        return new ArmaduraElfo();
    }
}
