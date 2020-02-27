import json
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.animation import Animation

from message.io_service import IoService


class RacerWidget(BoxLayout):
    name = StringProperty("nobody")
    speed_topic = StringProperty()
    distance_topic = StringProperty()
    race_distance = NumericProperty(1000)

    speed = NumericProperty(0)
    _speed_text = StringProperty('000 KPH')
    _distance = NumericProperty(0)
    _progress_text = StringProperty(f"0 / {race_distance.defaultvalue} M")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._io = IoService(__name__)
        self._io.start()

        self._speed_anim = None
        self._start_distance = None

    def reset_position(self):
        self._start_distance = self.distance

    def on_speed_data(self, speed_json: str):
        """
        :param speed_json: in meters per second
        """
        speed = json.loads(speed_json)
        speed_kph = speed * 3.6
        anim = Animation(speed=speed_kph, duration=1 / 5)
        anim.start(self)

    def on_speed(self, instance, value):
        self._speed_text = f"{value:06.2f} KPH"

    def on_distance_data(self, distance_json: str):
        distance = json.loads(distance_json)

        if self._start_distance is None:
            self._start_distance = distance

        self._distance = distance - self._start_distance
        self._update_progress_text()

    def _update_progress_text(self):
        if self._distance >= self.race_distance:
            self._progress_text = "FINISHED"
        else:
            self._progress_text = f"{self._distance:.2f} / {self.race_distance} M"

    def on_speed_topic(self, instance, value):
        self._io.subscribe(value, self.on_speed_data)

    def on_distance_topic(self, instance, value):
        self._io.subscribe(value, self.on_distance_data)


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
        value: root._distance
''')
