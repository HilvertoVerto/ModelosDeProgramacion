"""Gestor de buffs (Patrón Decorator)"""
import time


class BuffManager:
    """Gestiona buffs del jugador: frente, ropa y velocidad"""
    
    def __init__(self):
        self.front_level, self.front_expire = 0, 0
        self.clothes_type, self.clothes_expire = "traje", 0
        self.speed_level, self.speed_expire = 0, 0
        self.max_speed_level = 3

    def get_speed_multiplier(self):
        """Retorna multiplicador de velocidad según nivel"""
        multipliers = {0: 1.0, 1: 1.5, 2: 2.0, 3: 2.5}
        return multipliers.get(self.speed_level, 1.0)

    def apply_buff(self, buff_type, param, duration):
        """Aplica un buff al jugador"""
        now = time.time()
        
        if buff_type == "forehead":
            if self.front_level < 3:
                self.front_level += 1
            self.front_expire = now + duration
            
        elif buff_type == "clothes":
            transitions = {"traje": "vestido", "vestido": "caballeria"}
            self.clothes_type = transitions.get(self.clothes_type, self.clothes_type)
            self.clothes_expire = now + duration
                
        elif buff_type == "speed":
            if self.speed_level < self.max_speed_level:
                self.speed_level += 1
            self.speed_expire = now + duration

    def update(self):
        """Actualiza buffs, reduciendo niveles al expirar"""
        now = time.time()
        
        # Frente
        if self.front_expire and now >= self.front_expire:
            self.front_level = max(0, self.front_level - 1)
            self.front_expire = (now + 10) if self.front_level > 0 else 0
        
        # Ropa
        if self.clothes_expire and now >= self.clothes_expire:
            downgrades = {"caballeria": ("vestido", now + 10), "vestido": ("traje", 0)}
            if self.clothes_type in downgrades:
                self.clothes_type, self.clothes_expire = downgrades[self.clothes_type]
            else:
                self.clothes_expire = 0
        
        # Velocidad
        if self.speed_expire and now >= self.speed_expire:
            self.speed_level = max(0, self.speed_level - 1)
            self.speed_expire = (now + 10) if self.speed_level > 0 else 0