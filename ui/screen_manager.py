from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock

from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen


class RoldenSprintScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(RoldenSprintScreenManager, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(None, self, 'text')
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self._countdown = self.get_screen('countdown')
        self._countdown.bind(timer=self._on_countdown_timer)

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'spacebar':
            self.current = 'countdown'

    def _on_countdown_timer(self, instance, value):
        def switch_to_race(dt):
            self.current = 'race'

        if value <= 0:
            Clock.schedule_once(switch_to_race, 1 / 2)
