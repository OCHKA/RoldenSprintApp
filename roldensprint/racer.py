from time import time

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty


class SensorSample:
    def __init__(self, timestamp, rotations):
        self.timestamp = timestamp
        self.rotations = rotations


class Racer(EventDispatcher):
    name = StringProperty('nobody')
    speed = NumericProperty(0)
    distance = NumericProperty(0)

    def __init__(self, sensor, roller_length):
        super(Racer, self).__init__()

        self._sensor = sensor
        self._roller_length = roller_length
        self._prev_sample = None

    async def update(self):
        try:
            rotations = await self._sensor.poll()
            sample = SensorSample(rotations, time())
            self.update_props(sample)
            self._prev_sample = sample

        except Exception as e:
            print("racer: ", e)

    def update_props(self, sample):
        if not self._prev_sample:
            return

        time_period = sample.timestamp - self._prev_sample.timestamp
        rotations = sample.rotations - self._prev_sample.rotations

        self.speed = time_period / rotations
        self.distance += rotations * self._roller_length
