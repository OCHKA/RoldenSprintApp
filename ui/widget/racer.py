from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.animation import Animation

from core.component import Component


class RacerWidget(BoxLayout, Component):
    name = StringProperty("nobody")
    speed_topic = StringProperty()
    distance_topic = StringProperty()
    race_distance = NumericProperty(1000)

    speed = NumericProperty(0)
    distance = NumericProperty(0)

    _speed_text = StringProperty('000 KPH')
    _progress_text = StringProperty(f"0 / {race_distance.defaultvalue} M")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._speed_anim = None

    def reset_position(self):
        pass

    def on_speed_data(self, speed: int, **kwargs):
        """
        :param speed: in meters per second
        """

        speed_kph = speed * 3.6
        anim = Animation(speed=speed_kph, duration=1 / 5)
        anim.start(self)

    def on_speed(self, instance, value):
        self._speed_text = f"{value:06.2f} KPH"

    def on_distance_data(self, distance: int, **kwargs):
        """
        :param distance: since start in meters
        """

        anim = Animation(distance=distance, duration=1 / 5)
        anim.start(self)

    def on_distance(self, instance, value):
        self._progress_text = f"{value:.2f} / {self.race_distance} M"

    def on_speed_topic(self, instance, value):
        self._io.subscribe(value, self.on_speed_data)

    def on_distance_topic(self, instance, value):
        self._io.subscribe(value, self.on_distance_data)

    @property
    def is_finished(self):
        return self.distance >= self._start_distance


Builder.load_string('''
<LabelTemplate@Label>
    color: 0, 0, 0, 1
    font_size: '30sp'
    bold: True

<RacerWidget>:
    orientation: 'vertical'
    padding: 25, 25
    spacing: 25

    canvas:
        Color:
            rgba: 1, 1, 1, 1
        
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout: 
        size_hint: 1, 0.1
        orientation: 'horizontal'
        spacing: 25
        
        LabelTemplate:
            text: root.name
        LabelTemplate:
            text: root._speed_text
        LabelTemplate:
            text: root._progress_text
    
    ProgressBar:
        max: root.race_distance
        value: root.distance
''')
