import threading
import time
import logging

from ui.app import RoldenSprintApp
from sensor.roldensprint import RoldenSprintSensor
from converter.speed import SpeedConverter
from converter.distance import DistanceConverter


class RoldenSprint:
    def __init__(self):
        self.app = RoldenSprintApp()
        self.services = []

    def run(self):
        threading.Thread(target=self.init_components).start()
        self.app.run()

        for service in self.services:
            service.stop()

    def init_components(self):
        # wait for loading of config file
        while not self.app.config:
            time.sleep(1 / 10)

        base_url = self.app.config.get('sensor', 'url')
        max_poll_rate = self.app.config.getint('sensor', 'max_poll_rate')

        racer_index = 0
        for section in self.app.config:
            if 'racer' in section:
                self.init_racer(base_url, max_poll_rate, racer_index, section)
                racer_index += 1

    def init_racer(self, base_url: str, max_poll_rate: 30, index: int, section):
        racer = self.app.config[section]
        logging.info(f"init_racer: '{racer['name']}'")

        rotations = section + '.rotations'

        roller_length = racer.getint('roller_length_mm') / 1000
        speed = SpeedConverter(rotations, section + '.speed', roller_length)
        self.services.append(speed)

        distance = DistanceConverter(rotations, section + '.distance', roller_length)
        self.services.append(distance)


roldensprint = RoldenSprint()
roldensprint.run()
