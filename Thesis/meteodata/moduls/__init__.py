from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel
from .MeteodataMiner import MeteodataMiner
import time
from ..models import Meteodata, ForecastMeteodata, NeuralNet, Test
from ..forms import ForecastForm
from .Tester import Tester
from datetime import datetime
import numpy as np
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from .Deamon.NNBuilder import NNBuilder


class MainMenu:

    Miner = MeteodataMiner()
    SummaryModel = ForecastSummaryModel()
    ForecastModel = SimpleForecastModel()
    Tester = Tester()
    rows_count = 40

    def get_context():
        context = {}
        return context

    def magic():
        # len(list(self._correctWeatherDict.keys())) + 1
        dataPerc = MainMenu.SummaryModel._encode(list(Meteodata.objects.all().order_by('-datetime').values()[:500000]))
        objPerc = NNBuilder.buildAutoencoder_ForSummary(len(list(MainMenu.SummaryModel._correctWeatherDict)) + 1)
        objPerc.fit(dataPerc['train_values'], dataPerc['train_labels'], epochs=10, use_multiprocessing=True)
        predictResult = objPerc.predict(dataPerc['test_values'][:20])
        print(predictResult)
        predictResult = MainMenu.SummaryModel._decode(predictResult)
        print(predictResult)
        # MainMenu.SummaryModel._neuralNetObject = objPerc
        # MainMenu.SummaryModel.saveNet('newPerc')
        # RNN
        # dataRnn = MainMenu.ForecastModel._encode(list(Meteodata.objects.all().order_by('-datetime').values()[:500000]))
        # objRnn = MainMenu.ForecastModel.buildRnnNet()
        # objRnn.fit(dataRnn['train_values'], dataRnn['train_labels'], epochs=10, use_multiprocessing=True)
        # tmp = objRnn.predict(dataRnn['test_values'][:20])
        # print(type(tmp), type(tmp[0]), type(tmp[0][0]))
        # print(dataRnn['train_values'][:5], dataRnn['train_labels'][:5], dataRnn['test_values'][:5], dataRnn['test_labels'][:5])
        # predictResult = objRnn.predict(dataRnn['test_values'], verbose=1)
        # test_result = ''
        # sca = SparseCategoricalAccuracy()
        # sca.update_state(dataRnn['test_labels'], predictResult)
        # test_result = test_result + ' SparseCategoricalAccuracy: {} '.format(sca.result().numpy())
        # print(test_result)
        # MainMenu.ForecastModel._neuralNetObject = objRnn
        # MainMenu.ForecastModel.saveNet('newRnn')
        pass

    def data_update():
        print('data_update')
        MainMenu.Miner.updateMeteodata()
        
    def forecast_update():
        print('forecast_update')
        print('prepare data for forecast')
        date = datetime.now()
        lastdate = ForecastMeteodata.objects.all().order_by('-datetime').values_list('datetime').last()
        if not lastdate: 
            lastdate = Meteodata.objects.all().order_by('datetime').values_list('datetime').first()
        print('lastdate: ', lastdate)
        dataFull = list(Meteodata.objects.order_by('-datetime').filter(datetime__gte=str(lastdate[0])).values()[:10000])
        print('start forecast prediction: ', str(datetime.now() - date))
        resultMeteo = MainMenu.ForecastModel.predict(dataFull)
        print(resultMeteo[:10])
        for i in range(len(resultMeteo)):
            resultMeteo[i].update({
                dataFull[i]['datetime'],
                dataFull[i]['place']
            })
        print('start summary prediction: ', str(datetime.now() - date))
        resultSummary = MainMenu.SummaryModel.predict(resultMeteo) # TODO check result dict assembling
        result = []
        for i in range(len(resultSummary)):
            result.append({
                'datetime': dataFull[i]['datetime'],
                'place': dataFull[i]['place'],
                'place_name': dataFull[i]['place_name'],
                'temperature': resultMeteo[i]['temperature'],
                'wind_way': resultMeteo[i]['wind_way'],
                'wind_speed': resultMeteo[i]['wind_speed'],
                'air_pressure': resultMeteo[i]['air_pressure'],
                'water_pressure': resultMeteo[i]['water_pressure'],
                'weather': resultSummary[i]
            })
        print('finish forecast creation: ', str(datetime.now() - date))
        print(result[:40])
        # MainMenu._save_forecast(result)

    def make_test(examiner_id):
        print('make_nets_test')
        MainMenu.Tester.makeFullTest(examiner_id)

    def _save_forecast(data):
        print('forecast saving started')
        date = datetime.now()
        for row in data:
            form = ForecastForm(row)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        print('forecast saving finished: ', str(datetime.now() - date))

    def get_top_labels(modelObj, exeptionList=[]):
        labels = []
        fields = modelObj._meta.get_fields()
        for row in fields:
            if str(row.verbose_name) not in exeptionList:
                labels.append('' + row.verbose_name)
        return labels