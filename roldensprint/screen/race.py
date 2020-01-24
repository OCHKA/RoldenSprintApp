from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.app import App

from roldensprint.widget.racer import RacerWidget


class RaceScreen(Screen):
    pass


Builder.load_string('''
<RaceScreen>:
    name: 'race'
    
    BoxLayout:
        orientation: 'horizontal'
        
        RacerWidget:
            racer: app.racers[0]
            name: self.racer.name
            speed: self.racer.speed_ms * 3.6
            distance: self.racer.distance_m
            race_distance: app.race_distance_m
        
        RacerWidget:
            racer: app.racers[1]
            name: self.racer.name
            speed: self.racer.speed_ms * 3.6
            distance: self.racer.distance_m
            race_distance: app.race_distance_m
''')
