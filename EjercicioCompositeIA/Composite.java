import java.util.ArrayList;
import java.util.List;

// Interfaz Musical
interface Musical {
    void tocar();
    void afinar();
    void crear(Musical m);
    void eliminar(Musical m);
}

// Clase compuesta: Banda
class Banda implements Musical {
    private String nombre;
    private List<Musical> elementos = new ArrayList<>();

    public Banda(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public void tocar() {
        System.out.println("La banda " + nombre + " empieza a tocar:");
        for (Musical m : elementos) {
            m.tocar();
        }
    }

    @Override
    public void afinar() {
        System.out.println("La banda " + nombre + " está afinando:");
        for (Musical m : elementos) {
            m.afinar();
        }
    }

    @Override
    public void crear(Musical m) {
        elementos.add(m);
        System.out.println("Se agregó un nuevo elemento a la banda " + nombre);
    }

    @Override
    public void eliminar(Musical m) {
        elementos.remove(m);
        System.out.println("Se eliminó un elemento de la banda " + nombre);
    }
}

// Clase simple: Instrumento
abstract class Instrumento implements Musical {
    protected String nombre;

    public Instrumento(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public void crear(Musical m) {
        // No aplica en instrumento simple
        throw new UnsupportedOperationException("No se pueden agregar elementos a un instrumento simple.");
    }

    @Override
    public void eliminar(Musical m) {
        // No aplica en instrumento simple
        throw new UnsupportedOperationException("No se pueden eliminar elementos de un instrumento simple.");
    }

    @Override
    public void tocar() {
        System.out.println("El instrumento " + nombre + " está tocando.");
    }

    @Override
    public void afinar() {
        System.out.println("El instrumento " + nombre + " está afinando.");
    }
}

// Subclases de instrumentos
class Guitarra extends Instrumento {
    public Guitarra(String nombre) {
        super(nombre);
    }
}

class Tambor extends Instrumento {
    public Tambor(String nombre) {
        super(nombre);
    }
}

class Flauta extends Instrumento {
    public Flauta(String nombre) {
        super(nombre);
    }
}

// Clase principal para probar
public class Main {
    public static void main(String[] args) {
        // Creamos instrumentos
        Guitarra g1 = new Guitarra("Guitarra Eléctrica Roja");
        Guitarra g2 = new Guitarra("Guitarra Acústica Azul");
        Guitarra g3 = new Guitarra("Guitarra Clásica Marrón");

        Tambor t1 = new Tambor("Tambor Africano");
        Tambor t2 = new Tambor("Tambor de Guerra");
        Tambor t3 = new Tambor("Tambor Infantil");

        Flauta f1 = new Flauta("Flauta Dulce Blanca");
        Flauta f2 = new Flauta("Flauta de Pan Andina");
        Flauta f3 = new Flauta("Flauta Traversa Plateada");

        // Creamos una banda y agregamos instrumentos
        Banda banda = new Banda("Los Melódicos");
        banda.crear(g1);
        banda.crear(g2);
        banda.crear(g3);
        banda.crear(t1);
        banda.crear(t2);
        banda.crear(t3);
        banda.crear(f1);
        banda.crear(f2);
        banda.crear(f3);

        // Ejecutamos métodos
        banda.afinar();
        banda.tocar();
    }
}
