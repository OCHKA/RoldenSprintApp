from typing import List
from kivy.uix.screenmanager import Screen

from ui.widget.racer import RacerWidget
from ui.widget.graph import GraphWidget


class RaceScreen(Screen):
    def on_pre_enter(self, *args):
        if self.ids:
            self._reset_racers()

    def _reset_racers(self):
        racers: List[RacerWidget] = [self.ids[x] for x in self.ids if 'racer' in x]

        for racer in racers:
            racer.reset_position()
