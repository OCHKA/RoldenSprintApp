import json

from core import registry


# TODO: make config path more flexible
with open('roldensprint.json') as conf_file:
    conf = json.load(conf_file)

ui_racers = []

# startup per-racer infrastructure
for index, racer in enumerate(conf['racers']):
    def topic(path):
        return '.'.join(path)


    samples = topic(['sensor', str(index), 'sample'])
    speed = topic(['sensor', str(index), 'speed'])
    distance = topic(['sensor', str(index), 'distance'])

    ui_racers.append({'name': racer['name'], 'speed': speed, 'distance': distance})

    registry.register_component('converter.speed', input=samples, output=speed, length=racer['roller_length'])
    registry.register_component('converter.distance', input=samples, output=distance, length=racer['roller_length'])


registry.register_component('ui', race_distance=conf['sprint']['distance'], racers=ui_racers)
