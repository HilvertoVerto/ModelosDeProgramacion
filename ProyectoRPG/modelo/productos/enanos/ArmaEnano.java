package modelo.productos.enanos;

import modelo.productos.IArma;

public class ArmaEnano implements IArma {
    @Override
    public String obtenerDescripcion() {
    return "La espada de acero humano, forjada con disciplina y precisión. "
     + "Es un arma equilibrada, diseñada para la ofensiva y la defensa. "
     + "Aunque no posee encantamientos mágicos, su filo y durabilidad la convierten en una herramienta letal "
     + "en manos de un guerrero entrenado.";
    }
}
