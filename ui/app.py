from copy import copy
from kivy.app import App
from kivy.uix.screenmanager import FadeTransition
from kivy.context import get_current_context
from kivy.lang.builder import Builder

from core.component import Component

from .screen_manager import RoldenSprintScreenManager
from .expander_builder import ExpanderBuilder


class RoldenSprintApp(App, Component):
    screen: RoldenSprintScreenManager

    def __init__(self, race_distance, racers: list):
        super().__init__()

        self.race_distance = race_distance
        self.racers = racers

        context = copy(get_current_context())
        context['Builder'] = ExpanderBuilder(self, Builder, {'racers': self.racers})
        context.push()

    def build(self):
        context = get_current_context()
        context.pop()
        super(RoldenSprintApp, self).build()

        self.screen = RoldenSprintScreenManager(transition=FadeTransition())
        return self.screen

    def on_stop(self):
        self._io.publish('shutdown')
