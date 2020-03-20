from pathlib import Path
import sismic.io
import sismic.helpers
from sismic.interpreter import Interpreter

from core.component import Component
from .racer import Racer

SCRIPT_DIR = Path(__file__).resolve().parent


class RacerComponent(Component):
    def __init__(self, race_distance: int, sensor_distance: str, racer_distance: str, events: str):
        super().__init__()

        self._racer_distance_topic = racer_distance
        self._racer = Racer()

        with open(SCRIPT_DIR / 'racer.yaml') as f:
            statechart = sismic.io.import_from_yaml(f)

        context = {
            'race_distance': race_distance,
            'racer': self._racer
        }
        self._interpreter = Interpreter(statechart, initial_context=context)
        self._interpreter.execute()

        self._io.subscribe(sensor_distance, self._on_sensor_distance)
        self._io.subscribe(events, self._on_event)

    def _on_sensor_distance(self, distance: int):
        """
        :param distance: meters since sensor start
        """

        self._racer.sensor_distance = distance
        self._io.publish(self._racer_distance_topic, distance=self._racer.distance)

        steps = self._interpreter.execute()
        if steps:
            print(steps)

    def _on_event(self, name: str, **kwargs):
        self._interpreter.queue(name, **kwargs)
