NODE = """
<?xml version="1.0" encoding="UTF-8"?>
<osm version="0.6" generator="CGImap 0.7.5 (23439 thorn-02.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
 <node id="312892887" visible="true" version="7" changeset="44825099" timestamp="2017-01-01T15:57:42Z" user="Andrzej3345" uid="1875665" lat="52.2248972" lon="21.0152518">
  <tag k="amenity" v="restaurant"/>
  <tag k="contact:phone" v="+48 608707799"/>
  <tag k="contact:website" v="http://www.secado.com.pl"/>
  <tag k="cuisine" v="international"/>
  <tag k="name" v="Secado"/>
  <tag k="opening_hours" v="Mo-Th 11:00-23:00; Fr 11:00-24:00; Sa 00:00-01:00, 12:00-24:00; Su 00:00-01:00, 12:00-22:00"/>
 </node>
</osm>
""".strip()

GEOCODE = """
{
  "geocoding": {
    "version": "0.2",
    "attribution": "http://192.168.2.20:3100/attribution",
    "query": {
      "text": "Kraków",
      "size": 1,
      "layers": [
        "venue",
        "street",
        "country",
        "macroregion",
        "region",
        "county",
        "localadmin",
        "locality",
        "borough",
        "neighbourhood",
        "continent",
        "empire",
        "dependency",
        "macrocounty",
        "macrohood",
        "microhood",
        "disputed",
        "postalcode",
        "ocean",
        "marinearea"
      ],
      "private": false,
      "boundary.country": [
        "POL"
      ],
      "lang": {
        "name": "English",
        "iso6391": "en",
        "iso6393": "eng",
        "defaulted": true
      },
      "querySize": 20,
      "parser": "libpostal",
      "parsed_text": {
        "city": "kraków"
      }
    },
    "warnings": [
      "performance optimization: excluding 'address' layer"
    ],
    "engine": {
      "name": "Pelias",
      "author": "Mapzen",
      "version": "1.0"
    },
    "timestamp": 1578578908100
  },
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          19.987345,
          50.052652
        ]
      },
      "properties": {
        "id": "101752117",
        "gid": "whosonfirst:locality:101752117",
        "layer": "locality",
        "source": "whosonfirst",
        "source_id": "101752117",
        "name": "Krakow",
        "confidence": 1,
        "match_type": "exact",
        "accuracy": "centroid",
        "country": "Poland",
        "country_gid": "whosonfirst:country:85633723",
        "country_a": "POL",
        "region": "Lesser Poland Voivodeship",
        "region_gid": "whosonfirst:region:85687291",
        "region_a": "MA",
        "county": "M. Kraków",
        "county_gid": "whosonfirst:county:102079481",
        "locality": "Krakow",
        "locality_gid": "whosonfirst:locality:101752117",
        "continent": "Europe",
        "continent_gid": "whosonfirst:continent:102191581",
        "label": "Krakow, Poland"
      },
      "bbox": [
        19.8123365,
        49.9932915,
        20.1452955349,
        50.1163790318
      ]
    }
  ],
  "bbox": [
    19.8123365,
    49.9932915,
    20.1452955349,
    50.1163790318
  ]
}
""".strip()

CITY = """
{
  "name": "Kraków",
  "country": "Poland",
  "coordinates": [
    19.987345,
    50.052652
  ],
  "bbox": [
    19.9905307,
    50.0670603,
    19.9925743,
    50.0683756
  ]
}
""".strip()

POI = """
{
  "name": "Secado",
  "id": 312892887,
  "coordinates": [
    52.2248972,
    21.0152518
  ],
  "amenity": "restaurant",
  "opening hours": "Mo-Th 11:00-23:00; Fr 11:00-24:00; Sa 00:00-01:00, 12:00-24:00; Su 00:00-01:00, 12:00-22:00"
}
""".strip()
