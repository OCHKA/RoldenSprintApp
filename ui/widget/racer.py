import pynng
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.clock import Clock


class RacerWidget(BoxLayout):
    name = StringProperty("nobody")
    speed = NumericProperty(0)
    distance = NumericProperty(0)
    race_distance = NumericProperty(1000)
    sensor_index = NumericProperty(0)

    _progress_text = StringProperty(f"0 / {race_distance.defaultvalue} M")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._socket = pynng.Sub0(dial='inproc://roldensprint')
        self._socket.subscribe(f'sensor/{self.sensor_index}')
        Clock.schedule_once(self._poll)

    def _poll(self, dt):
        try:
            data = self._socket.recv(block=False)
        except pynng.exceptions.TryAgain:
            Clock.schedule_once(self._poll)
            return

        print(data)
        Clock.schedule_once(self._poll, 1 / 10)

    def on_distance(self, instance, value):
        if value >= self.race_distance:
            self._progress_text = "FINISHED"
        else:
            self._progress_text = f"{value:.2f} / {self.race_distance} M"


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
            text: str(int(root.speed)) + " KPH"
        LabelTemplate:
            text: root._progress_text
    
    ProgressBar:
        max: root.race_distance
        value: root.distance
''')
