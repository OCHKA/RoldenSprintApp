import time
import logging


class Racer:

    def __init__(self):
        self.start_time = None
        self.start_sensor_distance = None
        self.sensor_distance = 0

    @property
    def distance(self):
        if self.start_sensor_distance is None:
            self.reset()

        return self.sensor_distance - self.start_sensor_distance

    def reset(self):
        self.start_sensor_distance = self.sensor_distance
        self.start_time = time.time()

    def record_score(self):
        elapsed_time = time.time() - self.start_time
        logging.info(f"Racer: finished {self.distance:.0f} meters in {elapsed_time:.2f} seconds")
