from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label

from .sensor import CoapPeriodSensor


class RoldenSprint(App):
    rpm_label = Label(text="no data")
    sensor = CoapPeriodSensor()

    def build(self):
        Clock.schedule_interval(self.update, 1 / 30)
        return self.rpm_label

    def on_start(self):
        self.sensor.start()

    def update(self, dt):
        self.rpm_label.text = str(self.sensor.rpm)
