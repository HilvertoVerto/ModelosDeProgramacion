package controlador;

import modelo.fabricas.FabricaAbstracta;

public class FabricaManager {

    private static FabricaManager instancia;

    private FabricaAbstracta fabricaActiva;

    private FabricaManager() {}

    public static FabricaManager getInstancia() {
        if (instancia == null) {
            instancia = new FabricaManager();
        }
        return instancia;
    }

    public void setFabricaActiva(FabricaAbstracta fabrica) {
        this.fabricaActiva = fabrica;
    }

    public FabricaAbstracta getFabricaActiva() {
        return fabricaActiva;
    }
}