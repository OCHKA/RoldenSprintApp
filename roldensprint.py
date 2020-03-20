import json
from munch import munchify

from core.component import registry

# TODO: make config path more flexible
with open('roldensprint.json') as conf_file:
    conf = munchify(json.load(conf_file))

# per-racer infrastructure initialization
ui_racers = []

for index, racer in enumerate(conf.racers):
    def topic(path):
        return '.'.join(path)

    samples = topic(['sensor', str(index), 'sample'])
    speed = topic(['sensor', str(index), 'speed'])
    sensor_distance = topic(['sensor', str(index), 'distance'])

    registry.add('converter.speed', input=samples, output=speed, length=racer.roller_length)
    registry.add('converter.distance', input=samples, output=sensor_distance, length=racer.roller_length)

    racer_distance = topic(['racer', str(index), 'position'])
    events = topic(['racer', str(index), 'events'])

    registry.add(
        'sprint.racer',
        race_distance=conf.sprint.distance,
        sensor_distance=sensor_distance,
        racer_distance=racer_distance,
        events=events
    )
    ui_racers.append({'name': racer['name'], 'speed': speed, 'distance': racer_distance})

registry.add('ui', race_distance=conf.sprint.distance, racers=ui_racers)
