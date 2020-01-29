from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock


class CountDownScreen(Screen):
    timer = NumericProperty(3)
    _text = StringProperty('READY')

    def on_enter(self, *args):
        Clock.schedule_once(self._update, 1)

    def _update(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.timer = 0
            self._text = "GO"
        else:
            self._text = f"{self.timer:.2f}"
            Clock.schedule_once(self._update,  1 / 10)


Builder.load_string('''
<CountDownScreen>:
    name: 'countdown'

    BoxLayout:
        orientation: 'vertical'
        
        Label:
            text: 'countdown'
            size_hint: 1, 0.1
        Label:
            text: root._text
''')
