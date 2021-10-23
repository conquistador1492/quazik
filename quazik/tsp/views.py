from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from quazik.settings import GOOGLE_TOKEN

from typing import List
import requests


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        template_name = 'tsp/index.html'
        dct = {}
        return render(request, template_name, dct)


def number_of_cities(request):
    min_cities = 2
    max_cities = 20
    cities = int(request.POST.get('cities'))
    if cities < min_cities:  # or cities >= max_cities:
        dct = {'cities': cities, 'min_cities': min_cities, 'max_cities': max_cities}
        return render(request, 'tsp/incorrect_number_of_cities.html', dct)

    dct = {'cities': list(range(cities))}
    return render(request, 'tsp/choose_cities.html', dct)


class Marker:
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng


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

    print(f"Status code: {response.status_code}")
    print(f"Reason: {response.reason}")
    print(response.json())

    if response.status_code != 200:
        raise Exception(response.reason)

    distances = []
    for i, row in enumerate(response.json()['rows']):
        for j, value in enumerate(row['elements']):
            print(value)
            distances.append(Distance(markers[i], markers[j], value["duration"]['value']))

    return distances


class SolveTSP(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('We will solve soon')

    def post(self, request, *args, **kwargs):
        markers = []
        for symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if request.POST.get(symbol, None):
                lat, lng = request.POST.get(symbol).split(',')
                markers.append(Marker(symbol, lat, lng))

        if len(markers) < 2:
            return redirect('/')

        distances = return_distance_by_google_api(markers)

        return HttpResponse('|'.join([str(x) for x in distances]))

