package modelo.productos.orcos;

import modelo.productos.IMontura;

public class MonturaOrco implements IMontura {
    @Override
    public String obtenerDescripcion() {
    return "El lobo de guerra orco, una bestia salvaje criada en manadas. "
     + "Es feroz y difícil de domar, pero leal a su jinete orco. "
     + "Su velocidad y ferocidad lo convierten en un depredador letal en los campos de batalla.";

    }
}

