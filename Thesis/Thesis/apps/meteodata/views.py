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
        MainMenu.set_page(int(d['page']), 1)
        MainMenu.search(1, d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/meteodataview.html", context=context)
        except:
            return redirect('/meteodata/')


class ClearMeteodataChangePage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(1)
        MainMenu.set_page(int(d['page']), 2)
        MainMenu.search(2, d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/meteodataview.html", context=context)
        except:
            return redirect('/meteodata/')


class MeteodataSortPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.sort(1, int(d['field_name'][0]))
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/meteodataview.html", context=context)
        except:
            return redirect('/meteodata/')


class ClearMeteodataSortPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.sort(2, int(d['field_name'][0]))
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
        MainMenu.data_update()
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/meteodataview.html", context=context)
        except:
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
        MainMenu.set_page(int(d['page']), 3)
        MainMenu.search(3, d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/forecastview.html", context=context)
        except:
            return redirect('meteodata/forecast/')


class ClearForecastChangePage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(2)
        MainMenu.set_page(int(d['page']), 3)
        MainMenu.search(4, d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/forecastview.html", context=context)
        except:
            return redirect('meteodata/forecast/')


class ForecastSortPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.sort(3, int(d['field_name'][0]))
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/forecastview.html", context=context)
        except:
            return redirect('meteodata/forecast/')


class ClearForecastSortPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.sort(4, int(d['data_name'][0]))
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
        MainMenu.forecast_update()
        return redirect('meteodata/forecast/')


class ForecastUpdateTestResultPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.set_context(2)
        MainMenu.make_forecast_test()
        context = MainMenu.get_context()
        return render(request, "meteodata/testresultview.html", context=context)

    def get(self, request):
        d = request.GET
        print(d)
        MainMenu.set_context(2)
        MainMenu.make_forecast_test()
        context = MainMenu.get_context()
        return render(request, "meteodata/testresultview.html", context=context)


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
        MainMenu.set_page(int(d['page']), 5)
        MainMenu.search(5, d['search'])
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/analysisview.html", context=context)
        except:
            return redirect('meteodata/anoomaly/')


class AnomalySortPage(View):

    def post(self, request):
        d = request.POST
        print(d)
        MainMenu.sort(5, int(d['field_name'][0]))
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
        MainMenu.anomaly_update()
        try:
            context = MainMenu.get_context()
            return render(request, "meteodata/analysisview.html", context=context)
        except:
            return redirect('meteodata/anoomaly/')

