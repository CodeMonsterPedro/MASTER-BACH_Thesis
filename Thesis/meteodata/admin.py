from django.contrib import admin
from .models import Meteodata, ClearMeteodata, ClearForecastMeteodata, ForecastMeteodata, MeteodataAnomalies, Test, Test_Record, NeuralNet, Place

admin.site.register(Meteodata)
admin.site.register(ForecastMeteodata)
admin.site.register(ClearMeteodata)
admin.site.register(ClearForecastMeteodata)
admin.site.register(MeteodataAnomalies)
admin.site.register(Test)
admin.site.register(Test_Record)
admin.site.register(NeuralNet)
admin.site.register(Place)

# Register your models here.
