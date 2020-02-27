import random
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation

TIMER_TARGET_VALUE = 420
ENTER_TEXT = 'READY'


class CountDownScreen(Screen):
    text = StringProperty(ENTER_TEXT)
    timer = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anim = Animation

    def on_pre_enter(self, *args):
        self.timer = 0
        self.text = ENTER_TEXT

    def on_enter(self, *args):
        self._anim = Animation(timer=TIMER_TARGET_VALUE, duration=random.randint(2, 8))
        self._anim.start(self)

    def on_timer(self, instance, value):
        self.text = str(int(value))

    @property
    def is_finished(self) -> bool:
        return self.timer == TIMER_TARGET_VALUE
