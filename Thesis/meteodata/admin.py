from django.contrib import admin
from .models import Meteodata, ForecastMeteodata, Test, NeuralNet

admin.site.register(Meteodata)
admin.site.register(ForecastMeteodata)
admin.site.register(Test)
admin.site.register(NeuralNet)

# Register your models here.
