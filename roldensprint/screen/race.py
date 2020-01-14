from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

from roldensprint.widget import GraphWidget


class RaceScreen(Screen):
    pass


Builder.load_string('''
<RaceScreen>:
    name: 'sprint'

    BoxLayout:
        orientation: 'vertical'
        
        Label:
            text: 'fffg'
            size_hint: 1, 0.1

        GraphWidget:
            max_value: 15000
''')

