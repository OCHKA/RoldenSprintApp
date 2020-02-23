import asyncio

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from .sensor.coap import CoapSensor
from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen
from .racer import Racer


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
        if value <= 0:
            def switch_to_race(dt):
                self.current = 'race'

            Clock.schedule_once(switch_to_race, 1 / 2)


class RoldenSprintApp(App):
    screen = None
    sensor = None
    racers = [Racer(), Racer()]
    race_distance_m = 3000

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'racer_count': 2,
            'race_distance_m': self.race_distance_m
        })
        config.setdefaults('sensor', {
            'poll_freq_hz': 5
        })

        racer_count = config.getint('roldensprint', 'racer_count')
        for racer_id in range(racer_count):
            section = f'racer{racer_id}'

            config.setdefaults(section, {
                'name': f'SECT{racer_id}',
                'sensor_url': f'coap://192.168.4.1/rotations?{racer_id}',
                'roller_length_mm': 200
            })

    def build(self):
        Logger.info(f"App: Loaded configuration file <{self.get_application_config()}>")

        self.screen = RoldenSprintScreenManager(transition=FadeTransition())

        racer_count = self.config.getint('roldensprint', 'racer_count')

        for racer_id in range(racer_count):
            config_section = f'racer{racer_id}'
            config = self.config[config_section]

            sensor = CoapSensor(config.get('sensor_url'))
            roller_length_mm = config.getint('roller_length_mm')
            racer = Racer(config.get('name'), sensor, roller_length_mm / 1000)
            self.racers[racer_id] = racer

        self.race_distance_m = self.config.getint('roldensprint', 'race_distance_m')

        return self.screen

    def main(self):
        async def update_wrapper():
            try:
                while not self.config:  # wait for app to build
                    await asyncio.sleep(1 / 10)

                await self.update_racers()
            except asyncio.CancelledError:
                print("Racer updater was canceled")

        updater = asyncio.ensure_future(update_wrapper())

        async def main_wrapper():
            await self.async_run()
            updater.cancel()

        return asyncio.gather(main_wrapper(), updater)

    async def update_racers(self):
        poll_freq = self.config.getint('sensor', 'poll_freq_hz')

        while True:
            await asyncio.gather(*[racer.update() for racer in self.racers])
            await asyncio.sleep(1 / poll_freq)
