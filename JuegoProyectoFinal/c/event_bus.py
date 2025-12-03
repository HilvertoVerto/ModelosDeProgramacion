class EventBus:
    """Bus de eventos simple para desacoplar productores y consumidores."""

    def __init__(self):
        self._suscriptores = {}

    def suscribir(self, evento, callback):
        self._suscriptores.setdefault(evento, []).append(callback)

    def emitir(self, evento, payload=None):
        for callback in self._suscriptores.get(evento, []):
            callback(payload)
