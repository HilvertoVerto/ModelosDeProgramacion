import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

// ---------------------------------------------------------
// FASE 3: GlobalManager (Clase Dios corregida, sin números mágicos)
// ---------------------------------------------------------
public class GlobalManager {

    private static final double EXAMPLE_ORDER_TOTAL = 199.99;
    private static final double SAMPLE_WEIGHT_KG = 12.0;
    private static final double SAMPLE_DISTANCE_KM = 900.0;

    private final UserRepository userRepository;
    private final DiscountService discountService;
    private final ShippingService shippingService;

    public GlobalManager(UserRepository userRepository, DiscountService discountService, ShippingService shippingService) {
        this.userRepository = userRepository;
        this.discountService = discountService;
        this.shippingService = shippingService;
    }

    public void run() {
        List<User> users = userRepository.loadUsers();

        for (User u : users) {
            printUser(u);

            double discount = discountService.discountForOrder(u, EXAMPLE_ORDER_TOTAL);
            System.out.println("Descuento: " + discount);

            double domestic = shippingService.calculateShippingCost(
                    ShippingType.DOMESTIC,
                    SAMPLE_WEIGHT_KG,
                    SAMPLE_DISTANCE_KM
            );
            double international = shippingService.calculateShippingCost(
                    ShippingType.INTERNATIONAL,
                    SAMPLE_WEIGHT_KG,
                    SAMPLE_DISTANCE_KM
            );

            System.out.println("Envío nacional: " + domestic);
            System.out.println("Envío internacional: " + international);
            System.out.println("---------------------------------------");
        }
    }

    private void printUser(User u) {
        System.out.printf("[%s] %s - tier=%s%n", u.getId(), u.getName(), u.getTier());
    }

    public static void main(String[] args) {
        Path dbPath = Paths.get("users.csv");

        UserRepository userRepository = new UserRepository(dbPath);
        DiscountService discountService = new DiscountService();
        ShippingService shippingService = new ShippingService();

        new GlobalManager(userRepository, discountService, shippingService).run();
    }
}

// User: modelo de dominio
class User {
    private final String id;
    private final String name;
    private final String tier; // "gold", "silver", etc.

    public User(String id, String name, String tier) {
        this.id = id;
        this.name = name;
        this.tier = tier;
    }

    public String getId()   { return id; }
    public String getName() { return name; }
    public String getTier() { return tier; }
}

// UserRepository: acceso a datos (lectura de users.csv)
class UserRepository {

    private final Path dbPath;

    public UserRepository(Path dbPath) {
        this.dbPath = dbPath;
    }

    public List<User> loadUsers() {
        List<User> list = new ArrayList<>();
        if (!Files.exists(dbPath)) return list;

        try (BufferedReader br = Files.newBufferedReader(dbPath)) {
            String line;
            while ((line = br.readLine()) != null) {
                // CSV: id;name;tier
                String[] parts = line.split(";");
                String id   = parts.length > 0 ? parts[0] : "";
                String name = parts.length > 1 ? parts[1] : "";
                String tier = parts.length > 2 ? parts[2] : "";
                list.add(new User(id, name, tier));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return list;
    }
}

// DiscountService: lógica de descuentos (sin números mágicos)
class DiscountService {

    // Constantes en lugar de números mágicos
    private static final double GOLD_MIN_TOTAL = 200.0;
    private static final double GOLD_DISCOUNT_RATE = 0.20;
    private static final double SILVER_MIN_TOTAL = 50.0;
    private static final double SILVER_DISCOUNT_RATE = 0.10;

    public double discountForOrder(User user, double total) {
        String tier = user.getTier() != null ? user.getTier() : "";

        if ("gold".equalsIgnoreCase(tier) && total > GOLD_MIN_TOTAL) {
            return total * GOLD_DISCOUNT_RATE;
        }
        if ("silver".equalsIgnoreCase(tier) && total > SILVER_MIN_TOTAL) {
            return total * SILVER_DISCOUNT_RATE;
        }
        return 0.0;
    }
}

// ShippingType: tipo de envío (DOMÉSTICO / INTERNACIONAL)
enum ShippingType {
    DOMESTIC,
    INTERNATIONAL
}

// ShippingService: cálculo de envíos (duplicación + números mágicos corregidos)
class ShippingService {

    // Tarifas base
    private static final double BASE_DOMESTIC_FEE = 6.0;
    private static final double BASE_INTERNATIONAL_FEE = 8.0;

    // Factores de cálculo
    private static final double WEIGHT_FACTOR_PER_KG = 0.3;
    private static final double DISTANCE_DIVISOR_KM = 250.0;

    // Umbral de peso y recargos
    private static final double HEAVY_WEIGHT_THRESHOLD_KG = 15.0;
    private static final double DOMESTIC_HEAVY_SURCHARGE = 2.0; // > 15 kg
    private static final double INTERNATIONAL_HEAVY_SURCHARGE = 3.0; // >= 15 kg

    public double calculateShippingCost(ShippingType type,
                                        double weight,
                                        double distanceKm) {

        double baseFee = (type == ShippingType.DOMESTIC)
                ? BASE_DOMESTIC_FEE
                : BASE_INTERNATIONAL_FEE;

        double variable = weight * WEIGHT_FACTOR_PER_KG
                        + (distanceKm / DISTANCE_DIVISOR_KM);

        if (type == ShippingType.DOMESTIC && weight > HEAVY_WEIGHT_THRESHOLD_KG) {
            variable += DOMESTIC_HEAVY_SURCHARGE;
        }
        if (type == ShippingType.INTERNATIONAL && weight >= HEAVY_WEIGHT_THRESHOLD_KG) {
            variable += INTERNATIONAL_HEAVY_SURCHARGE;
        }

        return baseFee + variable;
    }
}
