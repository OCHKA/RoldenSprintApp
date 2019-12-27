from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock

from .sensor import CoapPeriodSensor
from .widget.rolling_graph import RollingGraph


class RoldenSprintWidget(BoxLayout):
    rpm = StringProperty("00000")


class RoldenSprintApp(App):
    refresh_rate = 1 / 30

    sensor = CoapPeriodSensor()
    widget = None

    def build(self):
        self.widget = RoldenSprintWidget()
        Clock.schedule_interval(self.update, self.refresh_rate)

        return self.widget

    def on_start(self):
        self.sensor.start()

    def update(self, dt):
        self.widget.rpm = f"{self.sensor.rpm:010}"
