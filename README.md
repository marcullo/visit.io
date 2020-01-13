# openrouteservice playground

Let's test and learn the [Optimization Service](https://openrouteservice.org/dev/#/api-docs/optimization).

## Requirements

- [openrouteservice](https://openrouteservice.org/dev/#/signup) account (on Firefox had problems once but on Chrome registered well).

- packages:

```
folium humanize numpy requests
```

## Getting started

1. Login to openrouteservice.
2. Request `TOKEN`.

**Note**: Beware of [limitations](https://openrouteservice.org/plans/). For now (12.12.2019) we have such limitations for endpoints.

- [GeocodeSearch](https://openrouteservice.org/dev/#/api-docs/geocode/search/get): 1000/day, 100/min.
- [Optimization](https://openrouteservice.org/dev/#/api-docs/optimization): 50/day, 10/min.

3. Prepare POIs to visit (N requests).
4. Optimize path:

```shell
./search.py --api_key TOKEN --params params/example.json
```

**Note**: You can change profile (way of transport), by selecting from the following (hopefully, because checked `driving car` and `foot-walking` only):

- `driving-car`
- `foot-walking`
- `cycling-regular`
- `cycling-road`
- (and some [more](https://github.com/GIScience/openrouteservice/wiki/Configuration-(app.config)#orsservicesroutingprofiles) might be in the future)

## Development

You can test either of api module by calling it.

```shell
./api/visualize.py
```
