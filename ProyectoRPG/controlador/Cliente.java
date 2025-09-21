package controlador;

import modelo.fabricas.*;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Paso 1: seleccionar raza
        System.out.println("=== Selección de Raza ===");
        System.out.println("1. Humanos");
        System.out.println("2. Elfos");
        System.out.println("3. Orcos");
        System.out.println("4. Enanos");
        System.out.print("Elige una opción: ");
        int opcionRaza = scanner.nextInt();

        FabricaManager manager = FabricaManager.getInstancia();

        switch (opcionRaza) {
            case 1 -> manager.setFabricaActiva(FabricaHumanos.getInstancia());
            case 2 -> manager.setFabricaActiva(FabricaElfos.getInstancia());
            case 3 -> manager.setFabricaActiva(FabricaOrcos.getInstancia());
            case 4 -> manager.setFabricaActiva(FabricaEnanos.getInstancia());
            default -> {
                System.out.println("Opción inválida. Se usarán Humanos por defecto.");
                manager.setFabricaActiva(FabricaHumanos.getInstancia());
            }
        }

        // Paso 2: seleccionar producto
        System.out.println("\n=== Selección de Producto ===");
        System.out.println("1. Cuerpo");
        System.out.println("2. Montura");
        System.out.println("3. Arma");
        System.out.println("4. Armadura");
        System.out.print("Elige una opción: ");
        int opcionProducto = scanner.nextInt();

        FabricaAbstracta fabrica = manager.getFabricaActiva();

        System.out.println("\n=== Objeto creado ===");
        switch (opcionProducto) {
            case 1 -> System.out.println(fabrica.crearCuerpo().obtenerDescripcion());
            case 2 -> System.out.println(fabrica.crearMontura().obtenerDescripcion());
            case 3 -> System.out.println(fabrica.crearArma().obtenerDescripcion());
            case 4 -> System.out.println(fabrica.crearArmadura().obtenerDescripcion()); 
            default -> System.out.println("Opción no válida.");
        }
    }
}
