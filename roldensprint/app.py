from kivy.properties import NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from .sensor.coap import CoapSensor
from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen


class RoldenSprintScreenManager(ScreenManager):
    speed = NumericProperty(0)

    def update(self, rpm):
        self.speed = rpm


class RoldenSprintApp(App):
    screen = None
    sensor = None
    players = 2

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'players': self.players,
        })
        config.setdefaults('sensor', {
            'url': '192.168.4.1/period',
            'poll_freq_hz': 10
        })
        self.players = config.getint('roldensprint', 'players')
        for player_id in range(self.players):
            config.setdefaults(f'player{player_id}', {
                'name': 'SECT',
                'wheel_length_mm': 2200,
                'roller_length_mm': 200
            })

    def build(self):
        poll_frq = self.config.get('sensor', 'poll_freq_hz')
        url = self.config.get('sensor', 'url')
        self.sensor = CoapSensor(url)

        self.screen = RoldenSprintScreenManager()

        return self.screen

    def on_start(self):
        self.sensor.start()

        def update_func(dt):
            self.screen.update(self.sensor.rpm)

        poll_freq = self.config.get('sensor', 'poll_freq_hz')
        Clock.schedule_interval(update_func, 1 / int(poll_freq))
