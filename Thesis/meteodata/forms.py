from django import forms

from .models import Meteodata, ForecastMeteodata, NeuralNet, Test


class MeteodataForm(forms.ModelForm):
    class Meta:
        model = Meteodata
        fields = (
            'datetime', 
            'place', 
            'place_name', 
            'temperature', 
            'wind_way', 
            'wind_speed', 
            'air_pressure', 
            'water_pressure', 
            'weather'
        )


class ForecastForm(forms.ModelForm):
    class Meta:
        model = ForecastMeteodata
        fields = (
            'datetime', 
            'place', 
            'place_name', 
            'temperature', 
            'wind_way', 
            'wind_speed', 
            'air_pressure', 
            'water_pressure', 
            'weather'
        )


class NeuralNetForm(forms.ModelForm):
    class Meta:
        model = NeuralNet
        fields = (
            'name', 
            'file_data', 
            'target', 
            'metric', 
            'description', 
            'conclusion'
        )


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = (
            'neuralnet_id', 
            'datetime', 
            'conclusion'
        )