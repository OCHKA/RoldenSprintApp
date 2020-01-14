from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder


class GraphWidget(Widget):
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


Builder.load_string('''
<GraphWidget>:
    canvas:
        Color:
            rgba: .4, .4, 1, 1
        Line:
            points: self.kv_points
            width: 1

''')
