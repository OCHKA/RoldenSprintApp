from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

TIMER_DEFAULT_VALUE = 3


class CountDownScreen(Screen):
    timer = NumericProperty(TIMER_DEFAULT_VALUE)

    def on_enter(self, *args):
        self.timer = TIMER_DEFAULT_VALUE
        Clock.schedule_once(self._update)

    def _update(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.timer = 0
            self.text = "GO"
        else:
            self.text = f"{self.timer:.2f}"
            Clock.schedule_once(self._update,  1 / 10)
