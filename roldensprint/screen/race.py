from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

from roldensprint.widget import RacerWidget


class RaceScreen(Screen):
    speed = NumericProperty(0)


Builder.load_string('''
<RaceScreen>:
    name: 'race'

    RacerWidget:
        name: 'racer1'
        speed: root.speed
''')
