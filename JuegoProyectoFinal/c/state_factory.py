from c.game_state import MenuState, PlayState, PauseState


class StateFactory:
    """Factory Method para crear estados del juego."""

    def __init__(self, event_bus, render, sprite_loader, input_handler, jugador, nivel):
        self.event_bus = event_bus
        self.render = render
        self.sprite_loader = sprite_loader
        self.input_handler = input_handler
        self.jugador = jugador
        self.nivel = nivel

    def crear_menu_state(self):
        return MenuState(self.event_bus, self.render)

    def crear_play_state(self):
        return PlayState(
            self.event_bus,
            self.render,
            self.sprite_loader,
            self.input_handler,
            self.jugador,
            self.nivel,
        )

    def crear_pause_state(self, play_state):
        return PauseState(self.event_bus, self.render, self.input_handler, play_state)
