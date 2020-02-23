import random

from kivy.properties import ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock


class GraphWidget(Widget):
    value = NumericProperty(0)
    max_value = NumericProperty(100)
    history_len = NumericProperty(1000)

    _points = ListProperty([])
    _history = ListProperty([0] * history_len.defaultvalue)

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)

        self.rand_red_color = random.random()
        Clock.schedule_once(self.update)

    def update(self, dt):
        self._history.append(self.value)
        if len(self._history) > self.history_len:
            self._history.pop(0)

        x_step = self.width / self.history_len
        y_step = self.height / self.max_value

        points = []
        for idx, value in enumerate(self._history):
            x_pos = x_step * idx + self.x
            y_pos = y_step * value + self.y
            points.append([x_pos, y_pos])
        self._points = points

        Clock.schedule_once(self.update)


Builder.load_string('''
<GraphWidget>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
            
        Rectangle:
            size: self.size
            pos: self.pos
            
        Color:
            rgba: 0, 0, 0, 1
            
        Line:
            points: root._points
            joint: 'round'
            width: 2.5
''')
