package modelo.productos.humanos;

import modelo.productos.IArmadura;

public class ArmaduraHumano implements IArmadura {
    @Override
    public String obtenerDescripcion() {
    return "La armadura de placas humana, forjada en acero resistente. "
        + "Ofrece una protección sólida contra ataques físicos, aunque sacrifica algo de movilidad. "
        + "Es ideal para soldados que se enfrentan a combates directos y prolongados, "
        + "brindando una defensa confiable en el campo de batalla.";  
    }
}
