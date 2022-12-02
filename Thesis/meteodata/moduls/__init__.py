from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel
from .MeteodataMiner import MeteodataMiner
import time
from ..models import Meteodata, ForecastMeteodata, NeuralNet, Test
from ..forms import ForecastForm
from .Tester import Tester


class MainMenu:

    Miner = MeteodataMiner()
    SummaryModel = ForecastSummaryModel()
    #ForecastModel = SimpleForecastModel('rnn', 'meteodata_meteodata')
    Tester = Tester()
    rows_count = 40
    

    def get_context():
        context = {}
        return context

    def data_update():
        print('data_update')
        MainMenu.Miner.updateMeteodata()
        
    def forecast_update():
        print('forecast_update')
        data = ForecastMeteodata.objects.all().order_by('datetime').last()
        #data = MainMenu.ForecastModel.predict(data)
        #data = MainMenu.SummaryModel.predict(data) TODO check result dict assembling
        #MainMenu._save_forecast(data)

    def make_test(examiners):
        print('make_nets_test')
        for examiner_id in examiners:
            Tester.makeFullTest(examiner_id)

    def _save_forecast(data):
        for row in data:
            d = {
                'datetime': row['fullDate'], 
                'place': row['city'], 
                'place_name': row['cityName'], 
                'temperature': row['Темп. Возд'], 
                'wind_way': row['Ветер'], 
                'wind_speed': row['Скор ветра'], 
                'air_pressure': row['Давл станц'], 
                'water_pressure': row['Давл моря'], 
                'weather': row['Явления погоды']
            }
            form = ForecastForm(d)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

    def get_top_labels(modelObj, exeptionList=[]):
        labels = []
        fields = modelObj._meta.get_fields()
        for row in fields:
            if str(row.verbose_name) not in exeptionList:
                labels.append('' + row.verbose_name)
        return labels