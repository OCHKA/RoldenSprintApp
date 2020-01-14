from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from . import GraphWidget


class RacerWidget(BoxLayout):
    name = StringProperty("nobody")
    speed = NumericProperty(0)
    _speed_history = ListProperty([0] * 420)
    _speed_text = StringProperty("00000")

    def on_speed(self, instance, new_value):
        self._speed_history.pop(0)
        self._speed_history.append(new_value)
        self._speed_text = f"{new_value:010}"


Builder.load_string('''
<RacerWidget>:
    orientation: 'vertical'

    BoxLayout:
        size_hint: 1, 0.1
        
        Label:
            text: root.name
        Label:
            text: root._speed_text

    GraphWidget:
        values: root._speed_history
        max_value: 15000
''')
