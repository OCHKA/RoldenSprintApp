from kivy.properties import ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock


class GraphWidget(Widget):
    value = NumericProperty(420)
    max_value = NumericProperty(2500)
    history_len = NumericProperty(1000)

    _points = ListProperty([])
    _history = [0] * history_len.defaultvalue

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.update)

    def update(self, dt):
        self._history.append(self.value)
        if len(self._history) > self.history_len:
            self._history.pop(0)

        x_step = self.width / self.history_len
        y_step = self.height / self.max_value

        points = []
        for idx, value in enumerate(self._history):
            x_pos = x_step * idx
            y_pos = y_step * value
            points.append([x_pos, y_pos])
        self._points = points

        Clock.schedule_once(self.update)


Builder.load_string('''
<GraphWidget>:
    canvas:
        Color:
            rgba: .4, .4, 1, 1
        Line:
            points: self._points
            width: 1
''')
