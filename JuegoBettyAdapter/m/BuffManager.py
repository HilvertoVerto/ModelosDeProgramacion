"""
Gestor de buffs usando PATRÓN DECORATOR

Este archivo gestiona los decoradores temporales y su aplicación.
Los decoradores reales están en PlayerDecorator.py
"""
import time
from m.PlayerDecorator import (
    ConcretePlayer,
    ForeheadDecorator,
    ClothesDecorator,
    SpeedDecorator
)


class BuffManager:
    """
    Gestor de decoradores temporales.
    
    Responsabilidades:
    1. Crear el componente base (ConcretePlayer)
    2. Aplicar decoradores (wrapping)
    3. Remover decoradores cuando expiran (unwrapping)
    4. Mantener el estado decorado actualizado
    """
    
    def __init__(self):
        # ===== COMPONENTE BASE =====
        self._base_player = ConcretePlayer()
        self._decorated_player = self._base_player
        
        # ===== CONTROL DE DECORADORES ACTIVOS =====
        self.active_decorators = {
            "forehead": {"level": 0, "expire": 0},
            "clothes": {"type": "traje", "expire": 0},
            "speed": {"level": 0, "expire": 0}
        }
        
        self.max_forehead_level = 3
        self.max_speed_level = 3

    def apply_buff(self, buff_type, param, duration):
        """
        Aplica un decorador temporal.
        
        Args:
            buff_type: "forehead", "clothes" o "speed"
            param: Parámetro del decorador
            duration: Duración en segundos
        """
        now = time.time()
        
        if buff_type == "forehead":
            # DECORADOR A: Frente
            current = self.active_decorators["forehead"]["level"]
            if current < self.max_forehead_level:
                self.active_decorators["forehead"]["level"] = current + 1
            self.active_decorators["forehead"]["expire"] = now + duration
            
        elif buff_type == "clothes":
            # DECORADOR B: Ropa
            transitions = {"traje": "vestido", "vestido": "caballeria"}
            current = self.active_decorators["clothes"]["type"]
            self.active_decorators["clothes"]["type"] = transitions.get(current, current)
            self.active_decorators["clothes"]["expire"] = now + duration
                
        elif buff_type == "speed":
            # DECORADOR C: Velocidad
            current = self.active_decorators["speed"]["level"]
            if current < self.max_speed_level:
                self.active_decorators["speed"]["level"] = current + 1
            self.active_decorators["speed"]["expire"] = now + duration
        
        # Reconstruir la cadena de decoradores
        self._rebuild_decorator_chain()

    def update(self):
        """
        Actualiza decoradores, removiendo los que expiran.
        (UNWRAPPING)
        """
        now = time.time()
        needs_rebuild = False
        
        # Verificar expiración de frente
        if self.active_decorators["forehead"]["expire"] > 0:
            if now >= self.active_decorators["forehead"]["expire"]:
                level = self.active_decorators["forehead"]["level"]
                self.active_decorators["forehead"]["level"] = max(0, level - 1)
                if self.active_decorators["forehead"]["level"] > 0:
                    self.active_decorators["forehead"]["expire"] = now + 10
                else:
                    self.active_decorators["forehead"]["expire"] = 0
                needs_rebuild = True
        
        # Verificar expiración de ropa
        if self.active_decorators["clothes"]["expire"] > 0:
            if now >= self.active_decorators["clothes"]["expire"]:
                downgrades = {"caballeria": ("vestido", now + 10), "vestido": ("traje", 0)}
                current = self.active_decorators["clothes"]["type"]
                if current in downgrades:
                    new_type, new_expire = downgrades[current]
                    self.active_decorators["clothes"]["type"] = new_type
                    self.active_decorators["clothes"]["expire"] = new_expire
                else:
                    self.active_decorators["clothes"]["expire"] = 0
                needs_rebuild = True
        
        # Verificar expiración de velocidad
        if self.active_decorators["speed"]["expire"] > 0:
            if now >= self.active_decorators["speed"]["expire"]:
                level = self.active_decorators["speed"]["level"]
                self.active_decorators["speed"]["level"] = max(0, level - 1)
                if self.active_decorators["speed"]["level"] > 0:
                    self.active_decorators["speed"]["expire"] = now + 10
                else:
                    self.active_decorators["speed"]["expire"] = 0
                needs_rebuild = True
        
        if needs_rebuild:
            self._rebuild_decorator_chain()

    def _rebuild_decorator_chain(self):
        """
        Reconstruye la cadena de decoradores.
        (WRAPPING)
        
        Orden: Base -> Frente -> Ropa -> Velocidad
        """
        # Empezar con el componente base
        player = self._base_player
        
        # DECORADOR A: Frente
        forehead_level = self.active_decorators["forehead"]["level"]
        if forehead_level > 0:
            player = ForeheadDecorator(player, level=forehead_level)
        
        # DECORADOR B: Ropa
        clothes_type = self.active_decorators["clothes"]["type"]
        if clothes_type != "traje":
            player = ClothesDecorator(player, clothes_type)
        
        # DECORADOR C: Velocidad
        speed_level = self.active_decorators["speed"]["level"]
        if speed_level > 0:
            multipliers = {1: 1.5, 2: 2.0, 3: 2.5}
            player = SpeedDecorator(player, multiplier=multipliers.get(speed_level, 1.0))
        
        # Guardar el jugador decorado
        self._decorated_player = player

    def get_decorated_player(self):
        """
        Retorna el jugador con todos los decoradores aplicados.
        Este es el método que usa el Modelo para obtener el estado decorado.
        """
        return self._decorated_player
    
    # ===== MÉTODOS DE COMPATIBILIDAD =====
    # (Para que funcione con el código existente de la Vista)
    
    @property
    def front_level(self):
        """Compatibilidad: retorna nivel de frente"""
        return self.active_decorators["forehead"]["level"]
    
    @property
    def front_expire(self):
        """Compatibilidad: retorna cuándo expira frente"""
        return self.active_decorators["forehead"]["expire"]
    
    @property
    def clothes_type(self):
        """Compatibilidad: retorna tipo de ropa"""
        return self.active_decorators["clothes"]["type"]
    
    @property
    def clothes_expire(self):
        """Compatibilidad: retorna cuándo expira ropa"""
        return self.active_decorators["clothes"]["expire"]
    
    @property
    def speed_level(self):
        """Compatibilidad: retorna nivel de velocidad"""
        return self.active_decorators["speed"]["level"]
    
    @property
    def speed_expire(self):
        """Compatibilidad: retorna cuándo expira velocidad"""
        return self.active_decorators["speed"]["expire"]
    
    def get_speed_multiplier(self):
        """Compatibilidad: retorna el multiplicador de velocidad actual"""
        speed_level = self.active_decorators["speed"]["level"]
        multipliers = {0: 1.0, 1: 1.5, 2: 2.0, 3: 2.5}
        return multipliers.get(speed_level, 1.0)