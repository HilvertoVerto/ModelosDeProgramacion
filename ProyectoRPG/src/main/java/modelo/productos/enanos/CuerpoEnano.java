package modelo.productos.enanos;

import modelo.productos.ICuerpo;

public class CuerpoEnano implements ICuerpo {
    @Override
    public String obtenerDescripcion() {
    return "De estatura baja (1,30 -- 1,45 m) y complexión muy robusta, con espalda ancha y alta densidad ósea. La piel suele estar curtida por el trabajo en la mina y la forja; barba larga y trenzada, a menudo adornada con anillos de metal que indican clan u oficio. Resistencia extraordinaria a la fatiga, buena tolerancia al frío y visión fiable en penumbra subterránea";

    }
}
