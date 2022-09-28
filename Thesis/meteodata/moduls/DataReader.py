from django.db.models.query_utils import select_related_descend
from ..models import Meteodata, ClearMeteodata, ForecastMeteodata, ClearForecastMeteodata, MeteodataAnomalies
from django.db.models import Q


class DataReader():

    def __init__(self):
        self._rows_count = 50
        self._meteodata_page = 1
        self._meteodata_search = ''
        self._meteodata = Meteodata.objects.all()
        self._meteodata_data = []
        self._meteodata_names = ['id', 'datetime', 'place', 'placeName', 'temperature', 'wind_way', 'wind_speed', 'air_pressure', 'water_pressure', 'weather']

        self._clear_meteodata_page = 1
        self._clear_meteodata_search = ''
        self._clear_meteodata = ClearMeteodata.objects.all()
        self._clear_meteodata_data = []

        self._forecast_page = 1
        self._forecast_search = ''
        self._forecast = ForecastMeteodata.objects.all()
        self._forecast_data = []
        self._forecastdata_names = ['id', 'datetime', 'place', 'placeName', 'temperature', 'wind_way', 'wind_speed', 'air_pressure', 'water_pressure', 'weather']

        self._clear_forecast_page = 1
        self._clear_forecast_search = ''
        self._clear_forecast = ClearForecastMeteodata.objects.all()
        self._clear_forecast_data = []
        
        self._anomaly_page = 1
        self._anomaly_search = ''
        self._anomaly = MeteodataAnomalies.objects.all()
        self._anomaly_data = []
        self._anomalydata_names = ['id', 'meteodata_id', 'fieldname', 'value', 'anomaly']

        self._firstOrderName = ''
        self._secondOrderName = ''
        self._thirdOrderName = ''
        self._fothOrderName = ''
        self._fifthOrderName = ''

        self._updateData(1)
        self._updateData(2)
        self._updateData(3)
        self._updateData(4)
        self._updateData(5)

    def get_data(self, dataId):
        print("get_data", dataId)
        if dataId == 1:
            return self._meteodata_data
        elif dataId == 2:
            return self._clear_meteodata_data
        elif dataId == 3:
            return self._forecast_data
        elif dataId == 4:
            return self._clear_forecast_data
        elif dataId == 5:
            return self._anomaly_data

    def set_page(self, tableId, num):
        print('set_page', tableId, num)
        if tableId == 1:
            self._meteodata_page = num
            self._updateData(1)
        elif tableId == 2:
            self._clear_meteodata_page = num
            self._updateData(2)
        elif tableId == 3:
            self._forecast_page = num
            self._updateData(3)
        elif tableId == 4:
            self._clear_forecast_page = num
            self._updateData(4)
        elif tableId == 5:
            self._anomaly_page = num
            self._updateData(5)

    def search(self, tableId, search):
        print('search')
        print(tableId, search, len(search))
        if tableId == 1:
            if search != '':
                self._meteodata_page = 1
                self._meteodata_search = search
                self._meteodata = self._meteodata.filter(
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
                if self._meteodata_search != '':
                    self._meteodata_page = 1
                self._meteodata_search = ''
                self._meteodata = Meteodata.objects.all().order_by('id')
            self._updateData(1)
        elif tableId == 2:
            self._clear_meteodata_page = 1
            if search != '':
                self._clear_meteodata_search = search
                self._clear_meteodata = self._clear_meteodata.filter(
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
                self._clear_meteodata_search = ''
                self._clear_meteodata = ClearMeteodata.objects.all().order_by('id')
            self._updateData(2)
        elif tableId == 3:
            self._forecast_page = 1
            if search != '':
                self._forecast_search = search
                self._forecast = self._forecast.filter(
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
                self._forecast_search = ''
                self._forecast = ForecastMeteodata.objects.all().order_by('id')
            self._updateData(3)
        elif tableId == 4:
            self._clear_forecast_page = 1
            if search != '':
                self._clear_forecast_search = search
                self._clear_forecast = self._clear_forecast.filter(
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
                self._clear_forecast_search = ''
                self._clear_forecast = ClearForecastMeteodata.objects.all().order_by('id')
            self._updateData(4)
        elif tableId == 5:
            self._anomaly_page = 1
            if search != '':
                self._anomaly_search = search
                self._anomaly = self._anomaly.filter(
                Q(id__contains=search) | 
                Q(meteodata_id__contains=search) | 
                Q(fieldname__contains=search) | 
                Q(value__contains=search) | 
                Q(anomaly__contains=search)
                )
            else:
                self._anomaly_search = ''
                self._anomaly = MeteodataAnomalies.objects.all().order_by('id')
            self._updateData(5)

    def get_max_pages(self, tableId):
        print('get_max_pages')
        size = 0
        if tableId == 1:
            size = self._meteodata.values('id').count()
        elif tableId == 2:
            size = self._clear_meteodata.values('id').count()  
        elif tableId == 3:
            size = self._forecast.values('id').count()
        elif tableId == 4:
            size = self._clear_forecast.values('id').count()     
        elif tableId == 5:
            size = self._anomaly.values('id').count()
        val = int(size // self._rows_count)
        if size % self._rows_count != 0:
            val += 1
        return val

    def sort(self, tableId, dataName):
        print('sort data', tableId, dataName)
        if tableId == 1:
            print(self._firstOrderName)
            if self._firstOrderName == '' or self._firstOrderName != dataName:
                self._meteodata = self._meteodata.order_by(self._meteodata_names[dataName])
                self._firstOrderName = dataName
            else:
                self._meteodata = self._meteodata.order_by(self._meteodata_names[self._firstOrderName]).reverse()
            self._meteodata_page = 1
            self._updateData(1)
        elif tableId == 2:
            print(self._secondOrderName)
            if self._secondOrderName == '' or self._secondOrderName != dataName:
                self._clear_meteodata = self._clear_meteodata.order_by(self._meteodata_names[dataName])
                self._secondOrderName = dataName
            else:
                self._clear_meteodata = self._clear_meteodata.order_by(self._meteodata_names[dataName]).reverse()
            self._clear_meteodata_page = 1
            self._updateData(2)
        elif tableId == 3:
            print(self._thirdOrderName)
            if self._thirdOrderName == '' or self._thirdOrderName != dataName:
                self._forecast = self._forecast.order_by(self._forecastdata_names[dataName])
                self._thirdOrderName = dataName
            else:
                self._forecast = self._forecast.order_by(self._forecastdata_names[dataName]).reverse()
            self._forecast_page = 1
            self._updateData(3)
        elif tableId == 4:
            print(self._fothOrderName)
            if self._fothOrderName == '' or self._fothOrderName != dataName:
                self._clear_forecast = self._clear_forecast.order_by(self._forecastdata_names[dataName])
                self._fothOrderName = dataName
            else:
                self._clear_forecast = self._clear_forecast.order_by(self._forecastdata_names[dataName]).reverse()  
            self._clear_forecast_page = 1
            self._updateData(4)
        elif tableId == 5:
            print(self._fifthOrderName)
            if self._fifthOrderName == '' or self._fifthOrderName != dataName:
                self._anomaly = self._anomaly.order_by(self._anomalydata_names[dataName])
                self._fifthOrderName = dataName
            else:
                self._anomaly = self._anomaly.order_by(self._anomalydata_names[dataName]).reverse()
            self._anomaly_page = 1
            self._updateData(5)

    def _updateData(self, tableId):
        print('updateData')
        print(self._meteodata_page, self._meteodata_search)
        if tableId == 1:
            self._meteodata_data = self._meteodata[((self._meteodata_page - 1) * self._rows_count):((self._meteodata_page - 1) * self._rows_count) + self._rows_count]
        elif tableId == 2:
            self._clear_meteodata_data = self._clear_meteodata[((self._clear_meteodata_page - 1) * self._rows_count):((self._clear_meteodata_page - 1) * self._rows_count) + self._rows_count]
        elif tableId == 3:
            self._forecast_data = self._forecast[((self._forecast_page - 1) * self._rows_count):(self._forecast_page * self._rows_count) + self._rows_count]
        elif tableId == 4:
            self._clear_forecast_data = self._clear_forecast[((self._clear_forecast_page - 1) * self._rows_count):((self._clear_forecast_page - 1) * self._rows_count) + self._rows_count]
        elif tableId == 5:
            self._anomaly_data = self._anomaly[((self._anomaly_page - 1) * self._rows_count):((self._anomaly_page - 1) * self._rows_count) + self._rows_count]
        print(type(self._meteodata))
