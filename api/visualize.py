#!/usr/bin/env python3
import folium
import json
import optimization_example
import os
import platform
import utils
import webbrowser
from functools import reduce
from logger import log
from marker import Marker
from optimization import Optimization
from poi import Poi


def _get_mass_center(points):
    return [sum([p[0] for p in points]) / len(points), sum([p[1] for p in points]) / len(points)]


def _create_map(markers):
    points = [m.coordinates for m in markers]

    start = markers[0]
    end = markers[-1]

    if start.id == end.id:
        log('visualize: same start and end')
        points.pop()

    center = _get_mass_center(points)

    log('visualize: points: {}'.format(points), verbose=True)
    log('visualize: center: {}'.format(center), verbose=True)

    return folium.Map(
        location=center,
        zoom_start=14,
        tiles='OpenStreetMap'
    )


def _create_markers(steps, pois):
    markers = []
    for step in steps:
        poi = Poi.from_id(pois, step.id)
        marker = Marker(poi, step)
        markers.append(marker)
    return markers


def _attach_markers(markers, gmap):
    start = markers[0]
    end = markers[-1]

    if start.id == end.id:
        start.set_end(end.arrival)

    for marker in markers[:-1]:
        marker.add_to_map(gmap)

    if start.id != end.id:
        end.add_to_map(gmap)


def _connect_markers(markers, gmap, vehicle):
    pairs_nr = len(markers) - 1

    for i in range(pairs_nr):
        m1 = markers[i]
        m2 = markers[i + 1]
        m1.connect(m2, gmap, pair_nr=i, vehicle=vehicle)


def _save_map(gmap, filename):
    gmap.save(filename)


def _run_map(filename):
    if platform.system().lower() == 'darwin':
        os.system(f'open /Applications/Safari.app {filename}')
        return

    webbrowser.open(filename)


def _log_stats(optimization):
    log('path: {}'.format(optimization.stats))


def _log_path(markers):
    path = ''
    header = 'path:'

    just_lengths = [3, 40, 10, 24, 10, 10, 20]
    columns = [
        '[ nr]',
        'node',
        'travel',
        'arrived',
        'wait',
        'visit',
        'opening hours'
    ]

    for i, c in enumerate(columns):
        header += ' {}'.format(c.ljust(just_lengths[i]))

    just_sum = reduce((lambda x, y: x + y + 1), just_lengths) + 1
    separator = 'path: {}'.format('-' * just_sum)

    log(separator)
    log(header)
    log(separator)

    for i, marker in enumerate(markers):
        index = '[{:>3}]'.format(str(i) if i > 0 and i < len(markers) - 1 else ' ↦ ' if i == 0 else ' ⇥ ')
        name = marker.name
        travel = str(markers[i - 1].get_travel_time(marker)) if i > 0 else ''
        arrival = str(marker.arrival) + ' ({})'.format(utils.dt2strday(marker.arrival))
        waiting = str(marker.waiting) if marker.waiting else ''
        visit = str(marker.duration) if marker.duration else ''
        opening_hours = marker.opening_hours if hasattr(marker, 'opening_hours') else ''

        row = 'path:'
        cells = [
            index,
            name,
            travel,
            arrival,
            waiting,
            visit,
            opening_hours
        ]

        for j, c in enumerate(cells):
            row += ' {}'.format(c.ljust(just_lengths[j]))

        log(row)


def visualize(optimization, pois):
    output_filename = 'optimization.html'
    log('optimization: {}'.format(optimization.computing_times))
    markers = _create_markers(steps=optimization.steps, pois=pois)
    gmap = _create_map(markers)
    _log_stats(optimization)
    _log_path(markers)

    _attach_markers(markers, gmap)
    _connect_markers(markers, gmap, vehicle=optimization.profile)
    _save_map(gmap, output_filename)
    _run_map(output_filename)


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

    visualize(optimization, pois)
