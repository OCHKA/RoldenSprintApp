from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from .sensor import CoapPeriodSensor
from .widget import RollingGraph
from .screen import SprintScreen


class RoldenSprintScreenManager(ScreenManager):
    pass


class RoldenSprintApp(App):
    screen = None

    rpm_history_window = 1000

    kv_rpm = StringProperty("00000")
    kv_rpm_history = ListProperty([0] * rpm_history_window)
    kv_sprint_countdown = NumericProperty(5)

    sensor = CoapPeriodSensor()

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'updates_per_second': 30
        })

    def build(self):
        self.screen = RoldenSprintScreenManager()

        updates_per_second = self.config.get('roldensprint', 'updates_per_second')
        refresh_rate = 1 / int(updates_per_second)
        Clock.schedule_interval(self.update, refresh_rate)

        return self.screen

    def build_settings(self, settings):
        settings.add_json_panel("RoldenSprint", self.config, filename='settings/roldensprint.json')

    def on_start(self):
        self.sensor.start()

    def update(self, dt):
        if self.kv_sprint_countdown - dt <= 0:
            self.kv_sprint_countdown = 0
        else:
            self.kv_sprint_countdown -= dt

        self.kv_rpm_history.pop(0)
        self.kv_rpm_history.append(self.sensor.rpm)

        self.kv_rpm = f"{self.sensor.rpm:010}"
