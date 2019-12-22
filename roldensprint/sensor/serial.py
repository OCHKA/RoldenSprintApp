import threading

from serial import Serial


class SerialSensor(threading.Thread):
    daemon = True

    __rpm = 0
    __port = Serial()
    __stop_event = threading.Event()

    def run(self) -> None:
        self.__port.port = '/dev/ttyUSB0'
        self.__port.baudrate = 115200
        self.__port.timeout = 1
        self.__port.open()

        while not self.__stop_event.is_set():
            line = self.__port.readline()
            self.__rpm = int(line)

    def stop(self):
        self.__stop_event.set()

    @property
    def rpm(self) -> int:
        return self.__rpm
