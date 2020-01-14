from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder


class GraphWidget(Widget):
    values = ListProperty([])
    max_value = 1000
    _points = ListProperty([])

    def calc_points(self, values):
        x_step = self.width / len(values)
        y_step = self.height / self.max_value

        points = []
        for idx, value in enumerate(values):
            x_pos = x_step * idx
            y_pos = y_step * value
            points.append([x_pos, y_pos])

        return points

    def on_values(self, instance, new_values):
        if not new_values:
            return
        self._points = self.calc_points(new_values)

    def on_size(self, instance, new_size):
        self._points = self.calc_points(self.values)


Builder.load_string('''
<GraphWidget>:
    canvas:
        Color:
            rgba: .4, .4, 1, 1
        Line:
            points: self._points
            width: 1

''')
