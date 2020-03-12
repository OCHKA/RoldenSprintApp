from pathlib import Path
import sismic.io
import sismic.helpers
from sismic.interpreter import Interpreter

from core.component import Component
from .racer import Racer

SCRIPT_DIR = Path(__file__).resolve().parent


class RacerComponent(Component):
    def __init__(self, race_distance: int, distance: str, position: str, events: str):
        super().__init__()

        self._position_topic = position
        self._racer = Racer(race_distance)

        with open(SCRIPT_DIR / 'racer.yaml') as f:
            statechart = sismic.io.import_from_yaml(f)
        self._interpreter = Interpreter(statechart, initial_context={'racer': self._racer})
        self._interpreter.execute()

        self._io.subscribe(distance, self._on_distance)
        self._io.subscribe(events, self._on_event)

    def _on_distance(self, distance: int):
        """
        :param distance: meters since sensor start
        """

        racer = self._racer

        racer.sensor_position = distance
        if racer.start_position is None:
            racer.start_position = distance
        racer.position = distance - racer.start_position

        self._io.publish(self._position_topic, distance=racer.position)

        steps = self._interpreter.execute()
        if steps:
            print(steps)

    def _on_event(self, name: str, **kwargs):
        self._interpreter.queue(name, **kwargs)
