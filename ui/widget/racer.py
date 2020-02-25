from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from pubsub import pub


class RacerWidget(BoxLayout):
    name = StringProperty("nobody")
    index = NumericProperty(0)
    race_distance = NumericProperty(1000)

    _speed = StringProperty('000 KPH')
    _distance = NumericProperty(0)
    _progress_text = StringProperty(f"0 / {race_distance.defaultvalue} M")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._start_distance = None

        pub.subscribe(self.on_speed_data, f'racer.{self.index}.speed')
        pub.subscribe(self.on_distance_data, f'racer.{self.index}.distance')

    def reset_position(self):
        self._start_distance = self.distance

    def on_speed_data(self, speed):
        speed_kph = speed * 3.6
        self._speed = f"{speed_kph:06.2f} KPH"

    def on_distance_data(self, distance):
        if self._start_distance is None:
            self._start_distance = distance

        self._distance = distance - self._start_distance
        self._update_progress_text()

    def _update_progress_text(self):
        if self._distance >= self.race_distance:
            self._progress_text = "FINISHED"
        else:
            self._progress_text = f"{self._distance:.2f} / {self.race_distance} M"


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
            text: root._speed
        LabelTemplate:
            text: root._progress_text
    
    ProgressBar:
        max: root.race_distance
        value: root._distance
''')
