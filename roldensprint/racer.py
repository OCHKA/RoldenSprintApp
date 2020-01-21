from kivy.properties import NumericProperty, StringProperty


class Racer:
    name = StringProperty('nobody')
    speed = NumericProperty(0)

    def __init__(self, sensor, roller_length):
        self._sensor = sensor
        self._roller_length = roller_length

    async def update(self):
        try:
            rotations = await self._sensor.poll()
        except Exception as e:
            print("racer: ", e)
        pass
