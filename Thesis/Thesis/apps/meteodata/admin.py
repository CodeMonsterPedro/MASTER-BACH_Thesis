from django.contrib import admin
from .models import Meteodata, ClearMeteodata, ClearForecastMeteodata, ForecastMeteodata, MeteodataAnomalies

admin.site.register(Meteodata)
admin.site.register(ForecastMeteodata)
admin.site.register(ClearMeteodata)
admin.site.register(ClearForecastMeteodata)
admin.site.register(MeteodataAnomalies)

# Register your models here.
