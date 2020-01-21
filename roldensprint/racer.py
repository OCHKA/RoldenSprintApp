from time import time

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty


class SensorSample:
    def __init__(self, timestamp: float, rotations: int):
        self.timestamp = timestamp
        self.rotations = rotations


class Racer(EventDispatcher):
    name = StringProperty('nobody')
    speed_ms = NumericProperty(0)
    distance_m = NumericProperty(0)

    def __init__(self, name: str, sensor, roller_length_m: int):
        super(Racer, self).__init__()

        self.name = name
        self._sensor = sensor
        self._roller_length_m = roller_length_m
        self._prev_sample = None

    async def update(self):
        try:
            rotations = await self._sensor.poll()
            sample = SensorSample(time(), rotations)
            self.update_props(sample)
            self._prev_sample = sample

        except Exception as e:
            print("racer: ", e)

    def update_props(self, sample):
        if not self._prev_sample:
            return

        time_period = sample.timestamp - self._prev_sample.timestamp
        rotations = sample.rotations - self._prev_sample.rotations

        self.speed_ms = rotations / time_period * self._roller_length_m
        self.distance_m += rotations * self._roller_length_m
