import time
from pubsub import pub


class SpeedConverter:
    """
    Converts samples of rotations to speed in ms
    """

    def __init__(self, rotations_topic: str, speed_topic: str, length: int):
        """
        :param rotations_topic: topic to listen for rotations data
        :param speed_topic: topic to send speed data
        :param length: length of circle in meters
        """

        self._rotations_topic = rotations_topic
        self._speed_topic = speed_topic

        self._length = length
        self._prev_timestamp = 0
        self._prev_rotations = 0

        pub.subscribe(self._on_update, rotations_topic)

    def _on_update(self, rotations):
        timestamp = time.time()

        if rotations == self._prev_rotations:
            return

        if self._prev_timestamp:
            speed_ms = self._convert(timestamp, rotations)
            pub.sendMessage(self._speed_topic, speed=speed_ms)

        self._prev_rotations = rotations
        self._prev_timestamp = timestamp

    def _convert(self, timestamp, new_rotations_value):
        elapsed_time = timestamp - self._prev_timestamp
        rotations = new_rotations_value - self._prev_rotations

        return rotations / elapsed_time * self._length
