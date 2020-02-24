import threading
import time
import logging

from ui.app import RoldenSprintApp
from sensor.roldensprint import RoldenSprint as RoldenSprintSensor


def init_sensors():
    base_url = app.config.get('sensor', 'url')
    max_poll_rate = app.config.getint('sensor', 'max_poll_rate')

    racer_index = 0
    for section in app.config:
        if 'racer' in section:
            logging.info(f"Starting sensor for '{section}'")
            rs_sensor = RoldenSprintSensor(base_url, racer_index, max_poll_rate)
            threading.Thread(target=rs_sensor.run).start()

            running_sensors.append(rs_sensor)
            racer_index += 1


def init_components():
    # wait for loading of config file
    while not app.config:
        time.sleep(1 / 10)

    init_sensors()


app = RoldenSprintApp()
running_sensors = []

threading.Thread(target=init_components).start()
app.run()

for sensor_to_stop in running_sensors:
    sensor_to_stop.stop()
