import time


class Racer:
    def __init__(self, race_distance):
        self.race_distance = race_distance

        self.start_time = None
        self.start_position = None

        self.sensor_position = 0
        self.position = 0

    def reset(self):
        self.position = 0
        self.start_position = self.sensor_position
        self.start_time = time.time()

    def record_score(self):
        print("score record placeholder")
