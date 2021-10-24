from typing import List

import requests
from django.db import models

from quazik.settings import GOOGLE_TOKEN


class Marker:
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.lat == other.lat and self.lng == other.lng

    def __hash__(self):
        return hash(self.name) + hash(self.lat) + hash(self.lng)


class Distance:
    def __init__(self, origin: Marker, destination: Marker, distance: float):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __str__(self):
        return ','.join([self.origin.name, self.destination.name, str(self.distance)])


def return_distance_by_google_api(markers: List[Marker]) -> List[Distance]:
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    origins = r'%7C'.join([
        f"{marker.lat}%2C{marker.lng}"
        for marker in markers
    ])
    destinations = r'%7C'.join([
        f"{marker.lat}%2C{marker.lng}"
        for marker in markers
    ])
    response = requests.get(f"{url}?origins={origins}&destinations={destinations}&key={GOOGLE_TOKEN}")

    if response.status_code != 200:
        raise Exception(response.reason)

    distances = []
    for i, row in enumerate(response.json()['rows']):
        for j, value in enumerate(row['elements']):
            distances.append(Distance(markers[i], markers[j], value["duration"]['value']))

    return distances