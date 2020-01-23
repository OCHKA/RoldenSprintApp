import asyncio

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger

from .sensor.coap import CoapSensor
from .screen.race import RaceScreen
from .screen.countdown import CountDownScreen
from .racer import Racer


class RoldenSprintScreenManager(ScreenManager):
    pass


class RoldenSprintApp(App):
    screen = None
    sensor = None
    racers = []

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'racer_count': 2,
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

        racer_count = self.config.getint('roldensprint', 'racer_count')

        for racer_id in range(racer_count):
            config_section = f'racer{racer_id}'
            config = self.config[config_section]

            sensor = CoapSensor(config.get('sensor_url'))
            roller_length_mm = config.getint('roller_length_mm')
            racer = Racer(config.get('name'), sensor, roller_length_mm / 1000)
            self.racers.append(racer)

        self.screen = RoldenSprintScreenManager()
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
