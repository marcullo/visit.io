#!/usr/bin/env python3
import folium
import json
import optimization_example
import webbrowser
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


def _connect_markers(markers, gmap):
    pairs_nr = len(markers) - 1

    for i in range(pairs_nr):
        m1 = markers[i]
        m2 = markers[i + 1]
        m1.connect(m2, gmap)


def _save_map(gmap, filename):
    gmap.save(filename)


def _run_map(filename):
    webbrowser.open(filename)


def visualize(optimization, pois):
    output_filename = 'optimization.html'
    markers = _create_markers(steps=optimization.steps, pois=pois)
    gmap = _create_map(markers)
    _attach_markers(markers, gmap)
    _connect_markers(markers, gmap)
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
    optimization = Optimization(content_optimization, pois_ids)

    visualize(optimization, pois)
