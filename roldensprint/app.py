from math import sin

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot

from .sensor import CoapPeriodSensor


class RoldenSprint(App):
    FPS = 1 / 30

    rpm_label = Label(size_hint=(1, .05))
    graph = Graph(xlabel="time", ylabel="rpm", y_grid=True, y_grid_label=True, x_ticks_major=25, y_ticks_major=1)
    layout = BoxLayout(orientation='vertical')

    plot = MeshLinePlot()
    plot_points = [(x, 50) for x in range(0, int(1 / FPS * 10))]

    sensor = CoapPeriodSensor()

    def build(self):
        self.plot.points = self.plot_points

        self.layout.add_widget(self.rpm_label)
        self.layout.add_widget(self.graph)

        Clock.schedule_interval(self.update, self.FPS)
        return self.layout

    def on_start(self):
        self.sensor.start()

    def update(self, dt):
        self.plot_points.append((self.plot_points[-1][0] + 1, self.sensor.rpm))
        self.plot_points.pop(0)
        self.graph.add_plot(self.plot)

        self.rpm_label.text = str(self.sensor.rpm)
