package modelo.productos.orcos;

import modelo.productos.ICuerpo;

public class CuerpoOrco implements ICuerpo {
    @Override
    public String obtenerDescripcion() {
    return "El cuerpo orco es imponente y musculoso. "
         + "Criados en un ambiente hostil, los orcos poseen una fuerza brutal y resistencia extraordinaria. "
         + "Son feroces en combate y priorizan el poder físico por encima de la estrategia.";
    }
}
