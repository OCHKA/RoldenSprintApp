import time

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
        self.speed = rpm[0]


class RoldenSprintApp(App):
    screen = None
    sensor = None
    players = 2

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'players': self.players,
        })
        config.setdefaults('sensor', {
            'poll_freq_hz': 3
        })

        self.players = config.getint('roldensprint', 'players')
        for player_id in range(self.players):
            config.setdefaults(f'player{player_id}', {
                'url': f'coap://192.168.4.1/period?{player_id}',
                'name': 'SECT',
                'wheel_length_mm': 2200,
                'roller_length_mm': 200
            })

    def build(self):
        sensor_urls = []
        for player_id in range(self.players):
            player = f'player{player_id}'
            sensor_urls.append(self.config.get(player, 'url'))

        poll_freq = self.config.getint('sensor', 'poll_freq_hz')
        self.sensor = CoapSensor(poll_freq, sensor_urls)

        self.screen = RoldenSprintScreenManager()
        return self.screen

    def on_start(self):
        self.sensor.start()

        def update_func(dt):
            self.screen.update(self.sensor.rpm)

        Clock.schedule_interval(update_func, 1 / self.sensor.poll_freq)
