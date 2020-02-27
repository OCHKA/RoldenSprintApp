import json

from message.io_service import IoService


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

        self._io = IoService(__name__)

        self._rotations_topic = rotations_topic
        self._speed_topic = speed_topic

        self._length = length
        self._rotations = 0
        self._timestamp = 0

        self._io.subscribe(rotations_topic, self._on_update)
        self._io.start()

    def _on_update(self, sensor_sample_json: str):
        # time in microseconds
        rotations, timestamp = json.loads(sensor_sample_json)

        if rotations == self._rotations:
            return

        # update speed
        if self._timestamp:
            speed_ms = self._convert(rotations - self._rotations, timestamp - self._timestamp)
            self._io.publish(self._speed_topic, json.dumps(speed_ms))

        # record increased distance
        self._timestamp = timestamp
        self._rotations = rotations

    def _convert(self, rotations, elapsed_time_usec):
        elapsed_time_s = elapsed_time_usec / 1e6
        distance_m = rotations * self._length
        return distance_m / elapsed_time_s
