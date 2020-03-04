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

    def __init__(self):
        super().__init__()

        context = copy(get_current_context())
        context['Builder'] = ExpanderBuilder(self, Builder, )
        context.push()

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'race_distance_m': 3000
        })
        config.setdefaults('sensor', {
            'url': f'coap://192.168.4.1/rotations',
            'max_poll_rate': 30
        })

        # default racer config. should be copy-pasted and re`name`d to add more racers
        config.setdefaults('racer0', {
            'name': f'SECT0',
            'roller_length_mm': 200
        })

    def build(self):
        context = get_current_context()
        context.pop()
        super(RoldenSprintApp, self).build()

        self.screen = RoldenSprintScreenManager(transition=FadeTransition())
        return self.screen

    def on_stop(self):
        self._io.publish('shutdown', None)
