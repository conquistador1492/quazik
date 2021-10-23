from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages


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
            # messages.error(request, 'Необходимо выбрать не менее двух городов')
            return redirect('/')

        return HttpResponse('\n'.join([str([marker.name, marker.lat, marker.lng]) for marker in markers]))

