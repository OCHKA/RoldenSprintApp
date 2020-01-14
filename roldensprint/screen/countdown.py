from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder


class CountDownScreen(Screen):
    pass


Builder.load_string('''
<CountDownScreen>:
    Label:
        text: 'koko screen'
        size_hint: 1, 0.1
''')
