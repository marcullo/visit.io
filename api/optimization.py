#!/usr/bin/env python3
import json
import optimization_example
from logger import log
from poi import Poi
from step import Step
from utils import i2dt


class Optimization:
    def __init__(self, content, pois_ids, profile):
        self.profile = profile

        status_code = content['code']

        if status_code == 3:
            raise RuntimeError('Routing failed!')
        elif status_code > 0:
            raise RuntimeError('Error code: {}'.format(status_code))

        unassigned_nr = len(content['unassigned'])

        if unassigned_nr > 0:
            log('Warning: {} unassigned targets'.format(unassigned_nr))

        route = content['routes'][0]

        self.visit_time = i2dt(route['service'])
        self.travel_time = i2dt(route['duration'])
        self.waiting_time = i2dt(route['waiting_time'])

        raw_steps = route['steps']
        self.steps = []
        for s in raw_steps:
            step = Step(s, pois_ids)
            self.steps.append(step)

        log(self, indent=0, verbose=True)

    def __repr__(self):
        return json.dumps({
            'profile': str(self.profile),
            'time': {
                'visit': str(self.visit_time),
                'travel': str(self.travel_time),
                'waiting': str(self.waiting_time) if self.waiting_time else None
            },
            'steps': [s.dict() for s in self.steps]
        }, indent=2)

    @property
    def stats(self):
        stats = []

        if self.visit_time:
            stats.append('{} sightseeing'.format(self.visit_time))
        if self.travel_time:
            stats.append('{} travel ({})'.format(self.travel_time, self.profile))
        if self.waiting_time:
            stats.append('{} waiting'.format(self.waiting_time))

        return str(stats)[1:-1].replace("'", '')


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

    content_optimization = json.loads(optimization_example.OPTIMIZATION)
    optimization = Optimization(content_optimization, pois_ids, profile='driving-car')
    print(optimization)
    print(optimization.stats)
