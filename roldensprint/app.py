from kivy.properties import StringProperty, ListProperty
from kivy.app import App
from kivy.clock import Clock

from .sensor import CoapPeriodSensor
from .widget.rolling_graph import RollingGraph


class RoldenSprintApp(App):
    refresh_rate = 1 / 30

    rpm_history_window = 1000

    kv_rpm = StringProperty("00000")
    kv_rpm_history = ListProperty([0] * rpm_history_window)

    sensor = CoapPeriodSensor()

    def build(self):
        Clock.schedule_interval(self.update, self.refresh_rate)

    def on_start(self):
        self.sensor.start()

    def update(self, dt):
        self.kv_rpm_history.pop(0)
        self.kv_rpm_history.append(self.sensor.rpm)

        self.kv_rpm = f"{self.sensor.rpm:010}"
