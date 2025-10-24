from abc import ABC, abstractmethod
from m.Constants import BASE_SPEED


# ============================================================
# COMPONENTE (Interfaz abstracta)
# ============================================================
class PlayerComponent(ABC):
    """
    COMPONENTE: Interfaz que define las operaciones 
    que pueden ser decoradas.
    """
    
    @abstractmethod
    def get_appearance(self):
        """Retorna la apariencia del jugador"""
        pass
    
    @abstractmethod
    def get_speed(self):
        """Retorna la velocidad del jugador"""
        pass
    
    @abstractmethod
    def get_description(self):
        """Retorna descripción del estado actual"""
        pass


# ============================================================
# COMPONENTE CONCRETO (Implementación base)
# ============================================================
class ConcretePlayer(PlayerComponent):
    """
    COMPONENTE CONCRETO: Implementación base de Don Armando.
    Sin ninguna decoración, es el jugador básico.
    """
    
    def __init__(self):
        # Estado base sin decoraciones
        self._base_clothes = "traje"
        self._base_forehead = 0
        self._base_speed = BASE_SPEED
    
    def get_appearance(self):
        """Apariencia base: traje y frente normal"""
        return {
            "clothes": self._base_clothes,
            "forehead": self._base_forehead
        }
    
    def get_speed(self):
        """Velocidad base sin modificar"""
        return self._base_speed
    
    def get_description(self):
        """Descripción del estado base"""
        return "Don Armando (base)"


# ============================================================
# DECORADOR BASE (Clase abstracta decoradora)
# ============================================================
class PlayerDecorator(PlayerComponent):
    """
    DECORADOR BASE: Envuelve un PlayerComponent y 
    delega las operaciones mientras permite modificarlas.
    """
    
    def __init__(self, player: PlayerComponent):
        self._wrapped_player = player
    
    def get_appearance(self):
        """Delega al componente envuelto"""
        return self._wrapped_player.get_appearance()
    
    def get_speed(self):
        """Delega al componente envuelto"""
        return self._wrapped_player.get_speed()
    
    def get_description(self):
        """Delega al componente envuelto"""
        return self._wrapped_player.get_description()


# ============================================================
# DECORADOR CONCRETO A: Frente
# ============================================================
class ForeheadDecorator(PlayerDecorator):
    """
    DECORADOR A: Agrega funcionalidad de frente grande.
    Modifica la apariencia del jugador sin cambiar el objeto base.
    """
    
    def __init__(self, player: PlayerComponent, level: int = 1):
        super().__init__(player)
        self._forehead_level = min(level, 3)  # Máximo 3
    
    def get_appearance(self):
        """DECORACIÓN: Modifica el nivel de frente"""
        appearance = self._wrapped_player.get_appearance()
        appearance["forehead"] = min(appearance["forehead"] + self._forehead_level, 3)
        return appearance
    
    def get_description(self):
        """Descripción con decoración"""
        base_desc = self._wrapped_player.get_description()
        return f"{base_desc} + Frente x{self._forehead_level}"


# ============================================================
# DECORADOR CONCRETO B: Ropa
# ============================================================
class ClothesDecorator(PlayerDecorator):
    """
    DECORADOR B: Agrega funcionalidad de cambio de ropa.
    Modifica la apariencia del jugador (categoría de sprites).
    """
    
    def __init__(self, player: PlayerComponent, clothes_type: str):
        super().__init__(player)
        self._clothes_type = clothes_type  # "vestido" o "caballeria"
    
    def get_appearance(self):
        """DECORACIÓN: Modifica el tipo de ropa"""
        appearance = self._wrapped_player.get_appearance()
        
        # Jerarquía: traje < vestido < caballeria
        hierarchy = {"traje": 0, "vestido": 1, "caballeria": 2}
        current_level = hierarchy.get(appearance["clothes"], 0)
        new_level = hierarchy.get(self._clothes_type, 0)
        
        # Solo cambia si es mayor en la jerarquía
        if new_level >= current_level:
            appearance["clothes"] = self._clothes_type
        
        return appearance
    
    def get_description(self):
        """Descripción con decoración"""
        base_desc = self._wrapped_player.get_description()
        clothes_name = "Vestido" if self._clothes_type == "vestido" else "Caballeria"
        return f"{base_desc} + {clothes_name}"


# ============================================================
# DECORADOR CONCRETO C: Velocidad
# ============================================================
class SpeedDecorator(PlayerDecorator):
    """
    DECORADOR C: Agrega funcionalidad de velocidad aumentada.
    Modifica las habilidades del jugador (velocidad de movimiento).
    """
    
    def __init__(self, player: PlayerComponent, multiplier: float = 1.5):
        super().__init__(player)
        self._speed_multiplier = multiplier
    
    def get_speed(self):
        """DECORACIÓN: Multiplica la velocidad"""
        base_speed = self._wrapped_player.get_speed()
        return base_speed * self._speed_multiplier
    
    def get_description(self):
        """Descripción con decoración"""
        base_desc = self._wrapped_player.get_description()
        return f"{base_desc} + Velocidad x{self._speed_multiplier}"