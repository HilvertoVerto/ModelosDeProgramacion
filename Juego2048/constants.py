import pygame

# Inicializar pygame
pygame.init()

# Constantes
FILAS = 6
COLUMNAS = 7
TAMANO_CELDA = 80
ANCHO = COLUMNAS * TAMANO_CELDA
ALTO = FILAS * TAMANO_CELDA + 100  # Espacio extra para instrucciones
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
ROJO = (255, 0, 0)

# Paleta de colores para bloques (estilo 2048)
COLOR_2 = (238, 228, 218)
COLOR_4 = (237, 224, 200)
COLOR_8 = (242, 177, 121)
COLOR_16 = (245, 149, 99)
COLOR_32 = (246, 124, 95)
COLOR_64 = (246, 94, 59)
COLOR_128 = (237, 207, 114)
COLOR_256 = (237, 204, 97)
COLOR_512 = (237, 200, 80)
COLOR_1024 = (237, 197, 63)
COLOR_2048 = (237, 194, 46)

# Configurar ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Bloques")
reloj = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 24)
