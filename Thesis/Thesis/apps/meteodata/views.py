from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from .models import Meteodata, ForecastMeteodata, MeteodataAnomalies
from django.db.models import Q
from .moduls import MainMenu


class MeteodataView(ListView):

    def get(self, request):
        MainMenu.set_context(1)
        context = MainMenu.get_context()
        return render(request, "meteodata/meteodataview.html", context=context)


class MeteodataChangePage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(1)
        MainMenu.set_count(int(d['count']))
        MainMenu.set_page(int(d['page']))
        MainMenu.search(d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/meteodataview.html", context=context)
        except:
            return redirect('/meteodata/')


class MeteodataUpdateDataPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(1)
        if not MainMenu._is_data_updated:
            MainMenu._data_update()
        return redirect('/meteodata/')


class ForecastView(ListView):

    def get(self, request):
        MainMenu.set_context(2)
        context = MainMenu.get_context()
        return render(request, "meteodata/forecastview.html", context=context)


class ForecastChangePage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(2)
        MainMenu.set_count(int(d['count']))
        MainMenu.set_page(int(d['page']))
        MainMenu.search(d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/forecastview.html", context=context)
        except:
            return redirect('meteodata/forecast/')


class ForecastUpdateDataPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(2)
        if not MainMenu._is_forecast_updated:
            MainMenu._make_forecast()
        return redirect('meteodata/forecast/')


class AnomalyView(ListView):

    def get(self, request):
        MainMenu.set_context(3)
        context = MainMenu.get_context()
        return render(request, "meteodata/analysisview.html", context=context)


class AnomalyChangePage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(3)
        MainMenu.set_count(int(d['count']))
        MainMenu.set_page(int(d['page']))
        MainMenu.search(d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/analysisview.html", context=context)
        except:
            return redirect('meteodata/anoomaly/')


class AnomalyUpdateDataPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(3)
        if not MainMenu.is_anomaly_updated:
            MainMenu._make_anomaly()
        return redirect('meteodata/anoomaly/')
