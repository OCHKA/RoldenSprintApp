import threading
import time
import logging

from ui.app import RoldenSprintApp
from sensor.roldensprint import RoldenSprintSensor
from converter.speed import SpeedConverter
from converter.distance import DistanceConverter

app = RoldenSprintApp()
sensors = []
converters = []


def init_racer(base_url: str, max_poll_rate: 30, index: int, racer):
    logging.info(f"init_racer: '{racer['name']}'")

    base_topic = f'racer.{index}'
    rotations = base_topic + '.rotations'

    sensor = RoldenSprintSensor(rotations, base_url, index, max_poll_rate)
    threading.Thread(target=sensor.run).start()
    sensors.append(sensor)

    roller_length = racer.getint('roller_length_mm') / 1000
    converters.append(SpeedConverter(rotations, base_topic + '.speed', roller_length))
    converters.append(DistanceConverter(rotations, base_topic + '.distance', roller_length))


def init_components():
    # wait for loading of config file
    while not app.config:
        time.sleep(1 / 10)

    base_url = app.config.get('sensor', 'url')
    max_poll_rate = app.config.getint('sensor', 'max_poll_rate')

    racer_index = 0
    for section in app.config:
        if 'racer' in section:
            init_racer(base_url, max_poll_rate, racer_index, app.config[section])
            racer_index += 1


threading.Thread(target=init_components).start()
app.run()

for sensor_to_stop in sensors:
    sensor_to_stop.stop()
