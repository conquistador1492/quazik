from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse

from tsp.models import Marker, return_distance_by_google_api
from tsp.solve_tsp_at_qboard import SolveTSPAtQBoard


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

        solver = SolveTSPAtQBoard(markers, distances)
        best_path = solver.get_best_path()

        return HttpResponse('->'.join([str(x) for x in best_path]))

