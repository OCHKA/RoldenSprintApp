import json
from message.io_service import IoService


class DistanceConverter:
    """
    Converts samples of rotations to distance in meters
    """

    def __init__(self, rotations_topic: str, distance_topic: str, length: int):
        """
        :param rotations_topic: topic to listen for rotations data
        :param distance_topic: topic to send distance data
        :param length: length of circle in meters
        """

        self._io = IoService(__name__)

        self._rotations_topic = rotations_topic
        self._distance_topic = distance_topic

        self._length = length

        self._io.subscribe(rotations_topic, self._on_update)
        self._io.start()

    def _on_update(self, rotations_json: str):
        rotations, timestamp = json.loads(rotations_json)

        distance = rotations * self._length
        self._io.publish(self._distance_topic, json.dumps(distance))
