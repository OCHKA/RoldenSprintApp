from kivy.properties import NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from .sensor import CoapSensor
from .screen import RaceScreen, CountDownScreen


class RoldenSprintScreenManager(ScreenManager):
    speed = NumericProperty(0)

    def update(self, rpm):
        self.speed = rpm


class RoldenSprintApp(App):
    screen = None
    sensor = CoapSensor()

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'updates_per_second': 30
        })

    def build(self):
        self.screen = RoldenSprintScreenManager()
        return self.screen

    def build_settings(self, settings):
        settings.add_json_panel("RoldenSprint", self.config, filename='settings/roldensprint.json')

    def on_start(self):
        self.sensor.start()

        updates_per_second = self.config.get('roldensprint', 'updates_per_second')
        refresh_rate = 1 / int(updates_per_second)

        def update_func(dt):
            self.screen.update(self.sensor.rpm)

        Clock.schedule_interval(update_func, refresh_rate)
