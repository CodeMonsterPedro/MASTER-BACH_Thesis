from ..models import Meteodata, ForecastMeteodata, MeteodataAnomalies
from django.db.models import Q


class MainMenu:

    currentContext = 1
    meteodata_page = 1
    meteodata_count = 50
    meteodata_search = ''
    is_data_updated = False
    meteodata = Meteodata.objects.all()
    forecast_page = 1
    forecast_count = 50
    forecast_search = ''
    is_forecast_updated = False
    forecast = ForecastMeteodata.objects.all()
    anomaly_page = 1
    anomaly_count = 50
    anomaly_search = ''
    is_anomaly_updated = False
    anomaly = MeteodataAnomalies.objects.all()

    def get_context():
        if MainMenu.currentContext == 1:
            context = {
                "meteodata_page": MainMenu.meteodata_page,
                "meteodata_count": MainMenu.meteodata_count,
                "meteodata_search": MainMenu.meteodata_search,
                "meteodata_max_pages": MainMenu.get_max_pages(),
                "meteodata_top_labels": MainMenu.get_top_labels(),
                "meteodata": MainMenu.meteodata[(MainMenu.meteodata_count * MainMenu.meteodata_page):(MainMenu.meteodata_count * MainMenu.meteodata_page) + MainMenu.meteodata_count]
            }
        elif MainMenu.currentContext == 2:
            context = {
                "forecast": MainMenu.forecast[(MainMenu.forecast_count * MainMenu.forecast_page):(MainMenu.forecast_count * MainMenu.forecast_page) + MainMenu.forecast_count],
                "forecast_page": MainMenu.forecast_page,
                "forecast_count": MainMenu.forecast_count,
                "forecast_search": MainMenu.forecast_search,
                "forecast_max_pages": MainMenu.get_max_pages(),
                "forecast_top_labels": MainMenu.get_top_labels()
            }
        elif MainMenu.currentContext == 3:
            context = {
                "anomaly": MainMenu.anomaly[(MainMenu.anomaly_count * MainMenu.anomaly_page):(MainMenu.anomaly_count * MainMenu.anomaly_page) + MainMenu.anomaly_count],
                "anomaly_page": MainMenu.anomaly_page,
                "anomaly_count": MainMenu.anomaly_count,
                "anomaly_search": MainMenu.anomaly_search,
                "anomaly_max_pages": MainMenu.get_max_pages(),
                "anomaly_top_labels": MainMenu.get_top_labels(),
            }
        context.update(
            {
                "menu_status": MainMenu.get_menu_status(),
                "submenu_status": MainMenu.get_submenu_status()
            }
        )
        return context

    def set_page(num):
        if MainMenu.currentContext == 1:
            MainMenu.meteodata_page = num
        elif MainMenu.currentContext == 2:
            MainMenu.forecast_page = num
        elif MainMenu.currentContext == 3:
            MainMenu.anomaly_page = num

    def set_count(num):
        if MainMenu.currentContext == 1:
            MainMenu.meteodata_count = num
        elif MainMenu.currentContext == 2:
            MainMenu.forecast_count = num
        elif MainMenu.currentContext == 3:
            MainMenu.anomaly_count = num

    def search(search):
        temp = 0
        if MainMenu.currentContext == 1:
            if search != '':
                MainMenu.meteodata_search = search
                MainMenu.meteodata = Meteodata.objects.filter(
                Q(id__contains=search) | 
                Q(datetime__contains=search) | 
                Q(place__contains=search) | 
                Q(placeName__contains=search) | 
                Q(temperature__contains=search) | 
                Q(wind_way__contains=search) | 
                Q(wind_speed__contains=search) | 
                Q(air_pressure__contains=search) | 
                Q(water_pressure__contains=search) | 
                Q(weather__contains=search)
                )
            else:
                MainMenu.meteodata = Meteodata.objects.all()
        elif MainMenu.currentContext == 2:
            if search != '':
                MainMenu.forecast_search = search
                MainMenu.forecast = ForecastMeteodata.objects.filter(
                Q(id__contains=search) | 
                Q(datetime__contains=search) | 
                Q(place__contains=search) | 
                Q(placeName__contains=search) | 
                Q(temperature__contains=search) | 
                Q(wind_way__contains=search) | 
                Q(wind_speed__contains=search) | 
                Q(air_pressure__contains=search) | 
                Q(water_pressure__contains=search) | 
                Q(weather__contains=search)
                )
            else:
                MainMenu.forecast = ForecastMeteodata.objects.all()
        elif MainMenu.currentContext == 3:
            if search != '':
                MainMenu.anomaly_search = search
                MainMenu.anomaly = MeteodataAnomalies.objects.filter(
                Q(id__contains=search) | 
                Q(meteodata_id__contains=search) | 
                Q(fieldname__contains=search) | 
                Q(value__contains=search) | 
                Q(anomaly__contains=search)
                )
            else:
                MainMenu.anomaly = MeteodataAnomalies.objects.all()

    def set_context(num):
        if num >= 1 and num <= 3:
            MainMenu.currentContext = num

    def data_update():
        print('data_update')

    def forecast_update():
        print('forecast_update')

    def anomaly_update():
        print('anomaly_update')

    def get_menu_status():
        print('get_menu_status')
        if MainMenu.currentContext == 1:
            return ['button-active', 'button', 'button']
        elif MainMenu.currentContext == 2:
            return ['button', 'button-active', 'button']
        elif MainMenu.currentContext == 3:
            return ['button', 'button', 'button-active']

    def get_submenu_status():
        print('get_submenu_status')
        if False:
            return 'timeout'
        return 'ready'

    def get_top_labels():
        print('get_top_labels')
        if MainMenu.currentContext == 1:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']
        elif MainMenu.currentContext == 2:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']
        elif MainMenu.currentContext == 3:
            return ['№', '№ метеоданных', 'Имя поля', 'Значение', 'Описание аномалии']

    def get_max_pages():
        print('get_max_pages')
        if MainMenu.currentContext == 1:
            size = len(Meteodata.objects.all())
            val = int(size // MainMenu.meteodata_count)
            if size % MainMenu.meteodata_count != 0:
                val += 1
            return val
        elif MainMenu.currentContext == 2:
            size = len(ForecastMeteodata.objects.all())
            val = int(size // MainMenu.forecast_count)
            if size % MainMenu.forecast_count != 0:
                val += 1
            return val        
        elif MainMenu.currentContext == 3:
            size = len(MeteodataAnomalies.objects.all())
            val = int(size // MainMenu.anomaly_count)
            if size % MainMenu.anomaly_count != 0:
                val += 1
            return val