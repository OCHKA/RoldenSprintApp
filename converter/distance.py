from pubsub import pub


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

        self._rotations_topic = rotations_topic
        self._distance_topic = distance_topic

        self._length = length

        pub.subscribe(self._on_update, rotations_topic)

    def _on_update(self, rotations):
        distance = rotations * self._length
        pub.sendMessage(self._distance_topic, distance=distance)
