package modelo.fabricas;

import modelo.productos.*;
import modelo.productos.humanos.*;

public class FabricaHumanos extends FabricaAbstracta {
    private static FabricaHumanos instancia;

    private FabricaHumanos() {}

    public static FabricaHumanos getInstancia() {
        if (instancia == null) {
            instancia = new FabricaHumanos();
        }
        return instancia;
    }

    @Override
    public ICuerpo crearCuerpo() {
        return new CuerpoHumano();
    }

    @Override
    public IMontura crearMontura() {
        return new MonturaHumano();
    }

    @Override
    public IArma crearArma() {
        return new ArmaHumano();
    }

    @Override
    public IArmadura crearArmadura() {
        return new ArmaduraHumano();
    }
}
