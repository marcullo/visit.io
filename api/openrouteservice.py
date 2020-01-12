import json
import requests
from logger import log


def request_point(name, api_key, city=None, osm_only=False):
    endpoint = 'https://api.openrouteservice.org/geocode/search'
    payload = {
        'api_key': api_key,
        'boundary.country': 'PL',
        'size': '1'
    }
    payload['text'] = name

    if osm_only:
        payload['sources'] = ['osm']

    if city:
        payload['boundary.rect.min_lon'] = city.bbox[0]
        payload['boundary.rect.min_lat'] = city.bbox[1]
        payload['boundary.rect.max_lon'] = city.bbox[2]
        payload['boundary.rect.max_lat'] = city.bbox[3]

    res = requests.get(endpoint, params=payload)
    res.raise_for_status()
    log('ors/geocode: got {}'.format(name))

    return res.json()


def request_node(id, api_key):
    endpoint = 'https://api.openstreetmap.org/api/0.6/node/{}'.format(id)
    res = requests.get(endpoint)
    res.raise_for_status()
    log('ors/node: got {}'.format(id))

    return res.text


def request_route_optimization(targets, params, profile, api_key):
    endpoint = 'https://api.openrouteservice.org/optimization'

    jobs = []
    for i, t, in enumerate(targets):
        jobs.append({
            'id': i,
            'location': t.coordinates[::-1],
            'service': t.duration,
            'time_windows': t.opening_timestamps
        })

    vehicles = [{
        'id': 0,
        'profile': profile,
        'start': params.from_coordinates[::-1],
        'end': params.to_coordinates[::-1],
        'time_window': [params.from_at, params.to_at]
    }]

    payload = {
        'jobs': jobs,
        'vehicles': vehicles
    }
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248ed4ab5fb3aca4d63a68c203ddd8fc8a5'
    }

    log('ors/optimization: profile: {}'.format(profile))
    log('ors/optimization: payload:', verbose=True)
    log(json.dumps(payload, indent=2), indent=0, verbose=True)

    res = requests.post(endpoint, json=payload, headers=headers)
    res.raise_for_status()
    log('ors/optimization: got:', verbose=True)
    log(json.dumps(res.json(), indent=2), indent=0, verbose=True)

    return res.json()
