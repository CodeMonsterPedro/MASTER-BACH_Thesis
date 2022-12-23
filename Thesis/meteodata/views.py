from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Meteodata, ForecastMeteodata, NeuralNet, Test
from django.db.models import Q
from .moduls import MainMenu
from .forms import NeuralNetForm


'''
GLOBAL TODO

Add 2 nets for forecast
Add 2 nets for summary
Add global factors analise method

'''

def update_meteodata(request):
    MainMenu.data_update()
    return redirect('meteodata')


def update_forecast(request):
    MainMenu.magic()
    return redirect('forecast')


class MeteodataView(ListView):

    model = Meteodata
    template_name = 'meteodata/meteodataview.html'
    context_object_name = 'Meteodata'
    paginate_by = MainMenu.rows_count
    ordering = ['-datetime']
    allow_empty = True
    meteodata_top_labels = MainMenu.get_top_labels(Meteodata)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Meteodata.objects.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'top_labels': self.meteodata_top_labels,
            'current_menu_page': 0
        })
        context.update(MainMenu.get_context())
        return context

    def post(self, request):
        if request.POST['reason'] == 'sort':
            if MeteodataView.ordering == request.POST['sort_option']:
                MeteodataView.ordering = '-' + str(request.POST['sort_option'])
            else:
                MeteodataView.ordering = request.POST['sort_option']
        return redirect('meteodata')


class ForecastView(ListView):

    model = ForecastMeteodata
    template_name = 'meteodata/forecastview.html'
    context_object_name = 'ForecastMeteodata'
    paginate_by = MainMenu.rows_count
    ordering = ['-datetime']
    allow_empty = True
    forecast_top_labels = MainMenu.get_top_labels(ForecastMeteodata)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = ForecastMeteodata.objects.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'top_labels': self.forecast_top_labels,
            'current_menu_page': 1
        })
        context.update(MainMenu.get_context())
        return context

    def post(self, request):
        if request.POST['reason'] == 'sort':
            if ForecastView.ordering == request.POST['sort_option']:
                ForecastView.ordering = '-' + str(request.POST['sort_option'])
            else:
                ForecastView.ordering = request.POST['sort_option']
        return redirect('forecast')


class NeuralnetView(ListView):

    model = NeuralNet
    template_name = 'meteodata/neuralnetsview.html'
    context_object_name = 'NeuralNet'
    paginate_by = MainMenu.rows_count
    ordering = ['name']
    allow_empty = True
    neuralnets_top_labels = MainMenu.get_top_labels(NeuralNet, ['NetFile',''])

    def get_queryset(self):
        qs = super().get_queryset()
        qs = NeuralNet.objects.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'Options' not in self.neuralnets_top_labels:
            self.neuralnets_top_labels.append('Options')
        context.update({
            'top_labels': self.neuralnets_top_labels,
            'current_menu_page': 2
        })
        context.update(MainMenu.get_context())
        return context

    def post(self, request):
        if request.POST['reason'] == 'sort':
            if NeuralnetView.ordering == request.POST['sort_option']:
                NeuralnetView.ordering = '-' + str(request.POST['sort_option'])
            else:
                NeuralnetView.ordering = request.POST['sort_option']
        elif request.POST['reason'] == 'addFile':
            print()
            data = {
                'name': request.FILES['file_data'].name.split('.')[0],  
                'target': request.POST['target'], 
                'metric': request.POST['metric'], 
                'description': request.POST['description'], 
                'conclusion': '-'
            }
            form = NeuralNetForm(data, request.FILES)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        elif request.POST['reason'] == 'test':
            MainMenu.make_test(int(request.POST['row_id']))
        elif request.POST['reason'] == 'remove':
            netfile = NeuralNet.objects.get(pk=int(request.POST['row_id']))
            netfile.delete()
        return redirect('neuralnets')


class TestsView(ListView):

    model = Test
    template_name = 'meteodata/testsview.html'
    context_object_name = 'Test'
    paginate_by = MainMenu.rows_count
    ordering = ['-datetime']
    allow_empty = True
    test_top_labels = MainMenu.get_top_labels(Test)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Test.objects.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'top_labels': self.test_top_labels,
            'current_menu_page': 3
        })
        context.update(MainMenu.get_context())
        return context

    def post(self, request):
        if request.POST['reason'] == 'sort':
            if TestsView.ordering == request.POST['sort_option']:
                TestsView.ordering = '-' + str(request.POST['sort_option'])
            else:
                TestsView.ordering = request.POST['sort_option']
        return redirect('tests')


