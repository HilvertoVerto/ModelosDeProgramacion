"""
Gestor de carga y caché de sprites
"""
import pygame
import os


def load_image(path, scale=1.0):
    """Carga y escala una imagen"""
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img


class SpriteLoader:
    """
    Gestor de sprites con caché para optimizar la carga.
    Maneja los sprites de Don Armando según categoría, nivel de frente y acción.
    """
    
    def __init__(self, sprites_root="graficos/Sprites"):
        self.root = sprites_root
        self.cache = {}

    def get(self, categoria, frente_index, action, frame_idx):
        """
        Obtiene un sprite desde el caché o lo carga si no existe.
        
        Args:
            categoria: "traje", "vestido" o "caballeria"
            frente_index: 0-3 (nivel de agrandamiento de frente)
            action: "mov" o "quieto"
            frame_idx: índice del frame (no usado actualmente)
        
        Returns:
            Surface de pygame con el sprite
        """
        key = (categoria, frente_index, action, frame_idx)
        if key in self.cache:
            return self.cache[key]

        folder = f"frente{frente_index}"
        base_names = {
            "traje": ("traje_mov_f{f}.png", "traje_quieto_f{f}.png"),
            "vestido": ("vestido_mov_f{f}.png", "vestido_quieto_f{f}.png"),
            "caballeria": ("cab_mov_f{f}.png", "cab_quieto_f{f}.png")
        }
        
        mov_name, quiet_name = base_names[categoria]
        fname = mov_name.format(f=frente_index) if action == "mov" else quiet_name.format(f=frente_index)
        path = os.path.join(self.root, categoria, folder, fname)
        
        surf = load_image(path, scale=0.6)
        self.cache[key] = surf
        return surf