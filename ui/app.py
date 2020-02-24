from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import FadeTransition

from .screen_manager import RoldenSprintScreenManager


class RoldenSprintApp(App):
    screen = None
    race_distance_m = 3000

    def build_config(self, config):
        config.setdefaults('roldensprint', {
            'race_distance_m': self.race_distance_m
        })
        config.setdefaults('sensor', {
            'url': f'coap://192.168.4.1/rotations',
            'max_poll_rate': 30
        })

        # default racer config. should be copy-pasted and re`name`d to add more racers
        config.setdefaults('racer0', {
            'name': f'SECT0',
            'roller_length_mm': 200
        })

    def build(self):
        Logger.info(f"App: Loaded configuration file <{self.get_application_config()}>")
        self.screen = RoldenSprintScreenManager(transition=FadeTransition())
        return self.screen
