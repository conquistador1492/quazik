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


class SolveTSP(generic.View):
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


class FoundedPath(generic.View):
    def post(self, request, *args, **kwargs):
        ...

