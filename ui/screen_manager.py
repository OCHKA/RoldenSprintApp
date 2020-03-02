from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen


class RoldenSprintScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(None, self, 'text')
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self._countdown = self.get_screen('countdown')
        self._countdown.bind(timer=self._on_countdown_timer)

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'spacebar':
            self.current = 'countdown'

    def _on_countdown_timer(self, instance, value):
        if self._countdown.is_finished:
            self.current = 'race'
