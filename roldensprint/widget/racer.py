from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from .graph import GraphWidget


class RacerWidget(BoxLayout):
    name = StringProperty("nobody")
    speed = NumericProperty(0)


Builder.load_string('''
<NameLabel@Label>
    color: 0, 0, 0, 1
    font_size: '30sp'
    bold: True

<RacerWidget>:
    orientation: 'vertical'
    canvas:
        Color:
            rgba: 1, 1, 1, 1

        Rectangle:
            size: self.size
            pos: self.pos
    padding: 5, 15

    BoxLayout:
        size_hint: 1, 0.1
        orientation: 'vertical'
        
        NameLabel:
            text: root.name
        NameLabel:
            text: str(int(root.speed)) + " KPH"

    GraphWidget:
        value: root.speed
        max_value: 80
''')
