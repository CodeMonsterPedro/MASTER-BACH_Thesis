from django.contrib import admin
from .models import Meteodata, ForecastMeteodata, MeteodataAnomalies

admin.site.register(Meteodata)
admin.site.register(ForecastMeteodata)
admin.site.register(MeteodataAnomalies)

# Register your models here.
