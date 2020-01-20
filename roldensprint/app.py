from kivy.properties import NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from .sensor.coap import CoapSensor
from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen


class RoldenSprintScreenManager(ScreenManager):
    speed = NumericProperty(0)

    def update(self, rpm):
        self.speed = rpm


class RoldenSprintApp(App):
    screen = None
    sensor = CoapSensor()

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'sensor_poll_freq': 30
        })

    def build(self):
        self.screen = RoldenSprintScreenManager()
        return self.screen

    def build_settings(self, settings):
        settings.add_json_panel("RoldenSprint", self.config, filename='settings/roldensprint.json')

    def on_start(self):
        self.sensor.start()

        def update_func(dt):
            self.screen.update(self.sensor.rpm)

        poll_freq = self.config.get('roldensprint', 'sensor_poll_freq')
        Clock.schedule_interval(update_func, 1 / int(poll_freq))
