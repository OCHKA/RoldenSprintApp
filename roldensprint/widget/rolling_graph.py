from kivy.properties import ListProperty
from kivy.uix.widget import Widget

from roldensprint import util


class RollingGraph(Widget):
    kv_points = ListProperty([])
    values = ListProperty([])
    max_value = 2500

    def on_values(self, instance, new_values):
        if not new_values:
            return

        x_step = self.width / len(new_values)
        y_step = self.height / self.max_value

        points = []
        for idx, value in enumerate(new_values):
            x_pos = x_step * idx
            y_pos = y_step * value
            points.append([x_pos, y_pos])

        self.kv_points = points


util.load_kv_file()
