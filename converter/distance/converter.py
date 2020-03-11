from core.component import Component


class DistanceConverter(Component):
    """
    Converts samples of rotations to distance in meters
    """

    def __init__(self, input: str, output: str, length: int):
        """
        :param input: topic to listen for rotations data
        :param output: topic to send distance data
        :param length: length of circle in meters
        """

        super().__init__()

        self._rotations_topic = input
        self._distance_topic = output

        self._length = length

        self._io.subscribe(self._rotations_topic, self._on_update)

    def _on_update(self, rotations: int, **kwargs):
        """
        :param rotations: number of rotations
        """

        distance = rotations * self._length
        self._io.publish(self._distance_topic, distance=distance)
