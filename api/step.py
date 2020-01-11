#!/usr/bin/env python3
import json
import optimization_example
from poi import Poi


class Step:
    def __init__(self, content, pois_ids):
        type = content['type']

        if type == 'start':
            self.id = pois_ids['start']
            self.start = True
        elif type == 'end':
            self.id = pois_ids['end']
            self.end = True
        else:
            self.id = pois_ids['visit'][content['job']]

        self.arrival = content['arrival']

        if 'waiting_time' in content:
            self.waiting = content['waiting_time']

        if 'service' in content:
            self.duration = content['service']

    def __repr__(self):
        return json.dumps(self.dict(), indent=2)

    def dict(self):
        content = {
            'id': self.id,
            'arrival': self.arrival
        }

        if hasattr(self, 'duration'):
            content['duration of stay'] = self.duration

        if hasattr(self, 'waiting'):
            content['waiting time'] = self.waiting

        return content


if __name__ == '__main__':
    pois = {
        'start': Poi('pois/Pętla Dworzec Centralny.json'),
        'end': Poi('pois/Pętla Dworzec Centralny.json'),
        'visit': [
            Poi('pois/U Szwejka.json'),
            Poi('pois/ORZO.json'),
            Poi('pois/Secado.json'),
            Poi('pois/Pomnik Wincentego Witosa.json')
        ]
    }

    pois_ids = {
        'start': pois['start'].id,
        'end': pois['end'].id,
        'visit': list(map(lambda p: p.id, pois['visit']))
    }

    content_steps = json.loads(optimization_example.STEPS)
    print('step by step:')
    for content in content_steps:
        step = Step(content, pois_ids)
        print(step)
