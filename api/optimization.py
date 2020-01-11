#!/usr/bin/env python3
import json
import optimization_example
from logger import log
from poi import Poi
from step import Step


class Optimization:
    def __init__(self, content, pois_ids):
        status_code = content['code']

        if status_code == 3:
            raise RuntimeError('Routing failed!')
        elif status_code > 0:
            raise RuntimeError('Error code: {}'.format(status_code))

        unassigned_nr = len(content['unassigned'])

        if unassigned_nr > 0:
            log('Warning: {} unassigned targets'.format(unassigned_nr))

        route = content['routes'][0]

        self.visit_time = route['service']
        self.travel_time = route['duration']
        self.waiting_time = route['waiting_time']

        raw_steps = route['steps']
        self.steps = []
        for s in raw_steps:
            step = Step(s, pois_ids)
            self.steps.append(step)

        log(self, indent=0, verbose=True)

    def __repr__(self):
        return json.dumps({
            'time': {
                'visit': self.visit_time,
                'travel': self.travel_time,
                'waiting': self.waiting_time
            },
            'steps': [s.dict() for s in self.steps]
        }, indent=2)


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

    content_optimization = json.loads(optimization_example.OPTIMIZATION)
    optimization = Optimization(content_optimization, pois_ids)
    print(optimization)
