package modelo.productos.elfos;

import modelo.productos.IArma;

public class ArmaElfo implements IArma {
    @Override
    public String obtenerDescripcion() {
    return "El arco élfico, tallado en maderas élficas y reforzado con magia ancestral. "
     + "Es un arma precisa que permite disparar flechas imbuidas en energía mágica. "
     + "Se dice que cada arco está ligado espiritualmente a su portador, "
     + "haciendo que sus disparos sean casi imposibles de esquivar.";

    }
}
