from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock

from .sensor import CoapPeriodSensor
from .widget.rolling_graph import RollingGraph


class RoldenSprintWidget(BoxLayout):
    rpm_history_window = 1000

    kv_rpm = StringProperty("00000")
    kv_rpm_history = ListProperty([0] * rpm_history_window)

    def update(self, rpm):
        self.kv_rpm_history.pop(0)
        self.kv_rpm_history.append(rpm)

        self.kv_rpm = f"{rpm:010}"


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
        self.widget.update(self.sensor.rpm)
