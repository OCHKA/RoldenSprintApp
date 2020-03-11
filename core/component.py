from .io.service import IoService


class Component:
    def __init__(self):
        self._io = IoService(self.__module__)
        self._io.start()
