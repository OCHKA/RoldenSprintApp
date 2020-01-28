from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.app import App

from roldensprint.widget.racer import RacerWidget
from roldensprint.widget.graph import GraphWidget


class RaceScreen(Screen):
    pass


Builder.load_string('''
<RacerTemplate@RacerWidget>:
    race_distance: app.race_distance_m

<RaceScreen>:
    name: 'race'
    
    racer0: app.racers[0]
    racer1: app.racers[1]
    speed_ms2kph: 3.6
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
        
            RacerTemplate:
                name: root.racer0.name
                speed: root.racer0.speed_ms * root.speed_ms2kph
                distance: root.racer0.distance_m
        
            RacerTemplate:
                name: root.racer1.name
                speed: root.racer1.speed_ms * root.speed_ms2kph
                distance: root.racer1.distance_m
        
        GraphWidget:
            index: 0
            value: root.racer0.speed_ms * root.speed_ms2kph
            max_value: 80
''')
