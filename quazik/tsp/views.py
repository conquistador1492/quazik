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


class Step:
    def __init__(self, origin_name, origin_lat, origin_lng, destination_name, destination_lat, destination_lng):
        self.origin_name = origin_name
        self.origin_lat = origin_lat
        self.origin_lng = origin_lng
        self.destination_name = destination_name
        self.destination_lat = destination_lat
        self.destination_lng = destination_lng


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

        print(best_path)

        steps = []
        for i in range(len(best_path) - 1):
            steps.append(Step(
                best_path[i].name, best_path[i].lat, best_path[i].lng,
                best_path[i + 1].name, best_path[i + 1].lat, best_path[i + 1].lng)
            )

        return render(request, 'tsp/founded_path.html', {'path': best_path, 'steps': steps})

