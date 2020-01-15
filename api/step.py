#!/usr/bin/env python3
import json
import optimization_example
from poi import Poi
from utils import i2dt, ts2dt


class Step:
    def __init__(self, content, pois_ids):
        type = content['type']

        self.start = False
        self.end = False
        self.arrival = ts2dt(content['arrival'])

        if type == 'start':
            self.id = pois_ids[0]
            self.start = True
        elif type == 'end':
            self.id = pois_ids[-1]
            self.end = True
        else:
            self.id = pois_ids[content['job'] + 1]

        if 'waiting_time' in content:
            self.waiting = i2dt(content['waiting_time'])

        if 'service' in content:
            self.duration = i2dt(content['service'])

    def __repr__(self):
        return json.dumps(self.dict(), indent=2)

    def dict(self):
        content = {
            'id': self.id,
            'arrival': str(self.arrival)
        }

        if hasattr(self, 'duration'):
            content['duration of stay'] = str(self.duration)

        if hasattr(self, 'waiting'):
            content['waiting time'] = str(self.waiting) if self.waiting else None

        return content


if __name__ == '__main__':
    pois = [
        Poi('pois/Pętla Dworzec Centralny.json'),
        Poi('pois/U Szwejka.json'),
        Poi('pois/ORZO.json'),
        Poi('pois/Secado.json'),
        Poi('pois/Pomnik Wincentego Witosa.json'),
        Poi('pois/Pętla Dworzec Centralny.json')
    ]
    pois_ids = list(map(lambda p: p.id, pois))

    content_steps = json.loads(optimization_example.OPTIMIZATION)['routes'][0]['steps']
    print('step by step:')
    for content in content_steps:
        step = Step(content, pois_ids)
        print(step)
