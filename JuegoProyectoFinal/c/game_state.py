import pygame
from m.entidad_factory import EntidadFactory
from m.buff_decorators import InvencibleBuff, SaltoBuff, VelocidadBuff
from m.buff_manager import BuffManager


class GameState:
    """Interfaz base para los estados del juego."""

    def manejar_eventos(self, eventos):
        raise NotImplementedError

    def actualizar(self):
        raise NotImplementedError

    def renderizar(self):
        raise NotImplementedError


class MenuState(GameState):
    """Estado de menu simple para iniciar o salir del juego."""

    def __init__(self, event_bus, render):
        self.event_bus = event_bus
        self.render = render
        self.fuente = pygame.font.SysFont("arial", 36)
        self.fuente_chica = pygame.font.SysFont("arial", 24)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.event_bus.emitir("cambiar_estado", "juego")
                elif evento.key == pygame.K_ESCAPE:
                    self.event_bus.emitir("salir")

    def actualizar(self):
        pass

    def renderizar(self):
        self.render.limpiar_pantalla()
        self.render.dibujar_suelo()

        mensaje = self.fuente.render("Demo estilo Mario", True, (255, 255, 255))
        subtitulo = self.fuente_chica.render(
            "ENTER para jugar  |  ESC para salir", True, (240, 240, 240)
        )

        ventana = self.render.ventana
        ventana.blit(
            mensaje, mensaje.get_rect(center=(self.render.ancho // 2, self.render.alto // 2 - 30))
        )
        ventana.blit(
            subtitulo, subtitulo.get_rect(center=(self.render.ancho // 2, self.render.alto // 2 + 10))
        )

        self.render.actualizar_pantalla()


class PlayState(GameState):
    """Estado principal de juego."""

    def __init__(self, event_bus, render, sprite_loader, input_handler, jugador, nivel):
        self.event_bus = event_bus
        self.render = render
        self.sprite_loader = sprite_loader
        self.input_handler = input_handler
        self.jugador = jugador
        self.nivel = nivel
        self.enemigos_data = list(self.nivel.enemigos)
        self.enemigos = EntidadFactory.crear_enemigos(self.enemigos_data)
        self.buffos_data = list(self.nivel.buffos)
        self.buffos = EntidadFactory.crear_buffos(self.buffos_data)
        self.proyectiles = []
        self.buff_classes = {
            "velocidad": VelocidadBuff,
            "salto": SaltoBuff,
            "invencible": InvencibleBuff,
        }
        self.buff_manager = BuffManager(self.buff_classes)
        self.buff_timers = {}
        self.limite_caida = self.render.alto + 150

    def reset(self):
        """Reinicia jugador, enemigos y camara."""
        spawn_x, spawn_y = self.nivel.spawn
        self.jugador.rect.x = spawn_x
        self.jugador.rect.y = spawn_y
        self.jugador.velocidad_x = 0
        self.jugador.velocidad_y = 0
        self.enemigos = EntidadFactory.crear_enemigos(self.enemigos_data)
        self.buffos = EntidadFactory.crear_buffos(self.buffos_data)
        self.proyectiles = []
        self.buff_manager.reset()
        self.buff_timers = {}
        self.jugador.reset_estadisticas()
        self.render.set_camara(0)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.event_bus.emitir("cambiar_estado", "menu")

        self.input_handler.manejar_movimiento(self.jugador)
        self.input_handler.manejar_salto(self.jugador)

    def actualizar(self):
        self.jugador.actualizar_frame_animacion(self.sprite_loader.get_num_frames())
        self.jugador.update(self.nivel.ancho_mundo, self.nivel.plataformas)

        for enemigo in self.enemigos:
            enemigo.update(self.nivel.plataformas)
            self.intentar_disparar(enemigo)

        self.actualizar_proyectiles()
        objetivo_camara = self.jugador.rect.centerx - self.render.ancho // 2
        limite = max(0, self.nivel.ancho_mundo - self.render.ancho)
        objetivo_camara = max(0, min(objetivo_camara, limite))
        self.render.set_camara(objetivo_camara)

        self.actualizar_buffs()
        self.verificar_pisar_enemigos()
        self.verificar_derrota()
        self.verificar_victoria()

    def intentar_disparar(self, enemigo):
        """Dispara proyectil si arma lo permite y jugador en alcance horizontal."""
        arma = getattr(enemigo, "arma", None)
        if not arma or arma.velocidad_proj == 0:
            return

        ahora = pygame.time.get_ticks()
        if ahora - enemigo.ultimo_disparo < arma.cooldown_ms:
            return

        distancia_x = abs(enemigo.rect.centerx - self.jugador.rect.centerx)
        if distancia_x > arma.alcance * 100:
            return

        direccion = 1 if self.jugador.rect.centerx >= enemigo.rect.centerx else -1
        proyectil = arma.crear_proyectil(enemigo.rect, direccion)
        if proyectil:
            enemigo.ultimo_disparo = ahora
            self.proyectiles.append(proyectil)

    def actualizar_proyectiles(self):
        """Mueve y limpia proyectiles activos."""
        vivos = []
        for proyectil in self.proyectiles:
            proyectil.update()
            if proyectil.vivo and -100 <= proyectil.rect.x <= self.nivel.ancho_mundo + 100:
                vivos.append(proyectil)
        self.proyectiles = vivos

    def actualizar_buffs(self):
        """Gestiona colision y expiracion de buffos."""
        restantes = []
        ahora = pygame.time.get_ticks()
        for buffo in self.buffos:
            if self.jugador.rect.colliderect(buffo.rect):
                self.buff_manager.activar(buffo.tipo, ahora)
            else:
                restantes.append(buffo)
        self.buffos = restantes
        self.buff_timers = self.buff_manager.aplicar(self.jugador, ahora)

    def verificar_pisar_enemigos(self):
        """Detecta si el jugador cae sobre un enemigo desde arriba y lo elimina."""
        if self.jugador.velocidad_y <= 0:
            # Solo detectar si el jugador está cayendo
            return

        enemigos_eliminados = []
        for enemigo in self.enemigos:
            if self.jugador.rect.colliderect(enemigo.rect):
                # Verificar si el jugador viene desde arriba
                # El jugador debe estar cayendo y su parte inferior debe estar cerca de la parte superior del enemigo
                margen_pisada = 15  # Pixeles de tolerancia para considerar que viene de arriba
                if self.jugador.rect.bottom - margen_pisada <= enemigo.rect.centery:
                    # El jugador pisó al enemigo desde arriba
                    enemigos_eliminados.append(enemigo)

                    # Hacer rebotar al jugador (como en Mario)
                    self.jugador.velocidad_y = -10  # Rebote al pisar enemigo

                    # Emitir evento de enemigo eliminado (patrón Observer)
                    self.event_bus.emitir("enemigo_eliminado", enemigo)

        # Eliminar enemigos pisados de la lista
        for enemigo in enemigos_eliminados:
            self.enemigos.remove(enemigo)

    def verificar_derrota(self):
        """Termina la partida si toca enemigo lateralmente o cae al vacio."""
        for enemigo in self.enemigos:
            if self.jugador.rect.colliderect(enemigo.rect) and not self.jugador.invencible:
                # Verificar si NO viene desde arriba (para no morir al pisar)
                margen_pisada = 15
                viene_desde_arriba = (self.jugador.velocidad_y > 0 and
                                     self.jugador.rect.bottom - margen_pisada <= enemigo.rect.centery)

                if not viene_desde_arriba:
                    self.event_bus.emitir("game_over")
                    return

        for proyectil in self.proyectiles:
            if proyectil.vivo and self.jugador.rect.colliderect(proyectil.rect) and not self.jugador.invencible:
                self.event_bus.emitir("game_over")
                return

        if self.jugador.rect.top > self.limite_caida:
            self.event_bus.emitir("game_over")

    def verificar_victoria(self):
        """Gana si llega a la meta."""
        if self.jugador.rect.right >= self.nivel.meta_x:
            self.event_bus.emitir("victoria")

    def renderizar(self):
        self.render.limpiar_pantalla()
        self.render.dibujar_suelo()
        self.render.dibujar_plataformas(self.nivel.plataformas)
        self.render.dibujar_enemigos(self.enemigos)
        self.render.dibujar_proyectiles(self.proyectiles)
        self.render.dibujar_buffos(self.buffos)
        self.render.dibujar_meta(self.nivel.meta_x)
        self.render.dibujar_buff_timers(self.buff_timers)

        sprite_jugador = self.sprite_loader.get_sprite(
            self.jugador.mirando_derecha,
            self.jugador.moviendo,
            self.jugador.frame_actual,
        )
        self.render.dibujar_jugador(self.jugador, sprite_jugador)
        self.render.actualizar_pantalla()
