package modelo.productos.enanos;

import modelo.productos.IMontura;

public class MonturaEnano implements IMontura {
    @Override
    public String obtenerDescripcion() {
    return "Carnero de guerra de montaña,"
    + " criado para escalada y embestida."
    + " Posee pezuñas duras para adherencia en roca,"
    + " pelaje denso contra el clima y cuernos reforzados con anillas metálicas ceremoniales."
    + " Mantiene el paso en pendientes pronunciadas y puede cargar brevemente para romper formaciones ligeras.";
    }
}
