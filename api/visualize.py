#!/usr/bin/env python3
import folium
import json
import optimization_example
import utils
import types
import webbrowser
from logger import log
from optimization import Optimization
from poi import Poi


def _get_mass_center(points):
    return [sum([p[0] for p in points]) / len(points), sum([p[1] for p in points]) / len(points)]


def _create_map(points):
    center = _get_mass_center(points)

    log('visualize: points: {}'.format(points), verbose=True)
    log('visualize: center: {}'.format(center), verbose=True)

    return folium.Map(
        location=center,
        zoom_start=14,
        tiles='OpenStreetMap'
    )


def _define_markers(steps, pois):
    markers = []

    for step in steps:
        marker = types.SimpleNamespace()

        id = step.id
        poi_candidates = [poi for poi in pois if poi.id == id]

        if len(poi_candidates) == 0:
            raise AssertionError('Poi for step id {} not found!'.format(id))

        poi = poi_candidates[0]
        marker.coordinates = poi.coordinates
        marker.popup = poi.name
        marker.tooltip = poi.name

        markers.append(marker)

    return markers


def _get_icons(pois_nr):
    icons = []

    # start
    icons.append(folium.Icon(icon='home'))

    for i in range(pois_nr):
        icons.append(None)

    icons.append(folium.Icon(icon='home'))

    return icons


def _attach_markers(gmap, markers, icons):
    for marker, icon in zip(markers, icons):
        if icon is not None:
            folium.Marker(marker.coordinates, popup=marker.popup, tooltip=marker.tooltip, icon=icon).add_to(gmap)
        else:
            folium.Marker(marker.coordinates, popup=marker.popup, tooltip=marker.tooltip).add_to(gmap)


def _attach_path(gmap, points):
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        folium.PolyLine(locations=[p1, p2]).add_to(gmap)
        arrows = utils.get_arrows(locations=[p1, p2], n_arrows=1)

        for arrow in arrows:
            arrow.add_to(gmap)


def _save_map(gmap, filename):
    gmap.save(filename)


def _run_map(filename):
    webbrowser.open(filename)


def visualize(optimization, pois):
    output_filename = 'optimization.html'

    start = pois['start']
    end = pois['end']
    pois = pois['visit']

    points = [start.coordinates]
    points.extend([poi.coordinates for poi in pois])
    points.append(end.coordinates)

    pois_with_start_end = [start]
    pois_with_start_end.extend(pois)
    pois_with_start_end.append(end)

    gmap = _create_map(points)
    markers = _define_markers(optimization.steps, pois_with_start_end)
    icons = _get_icons(len(pois))
    _attach_markers(gmap, markers, icons)
    _attach_path(gmap, points)
    _save_map(gmap, output_filename)
    _run_map(output_filename)


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

    visualize(optimization, pois)
