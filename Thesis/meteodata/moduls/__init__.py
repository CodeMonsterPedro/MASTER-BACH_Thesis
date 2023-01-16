from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel
from .MeteodataMiner import MeteodataMiner
import time
from ..models import Meteodata, ForecastMeteodata, NeuralNet, Test
from ..forms import ForecastForm
from .Tester import Tester
from datetime import datetime
import numpy as np
from tensorflow.keras.metrics import Precision
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
        task = 'F'
        modelType = 'RF'
        data = list(Meteodata.objects.all().order_by('-datetime').values()[:500000])
        modelObj = []
        if task == 'S':
            data = MainMenu.SummaryModel._encode(data)
        else:
            data = MainMenu.ForecastModel._encode(data)
        if modelType == 'PS':
            modelObj = NNBuilder.buildPerceptronNet()
        elif modelType == 'PF':
            modelObj = NNBuilder.buildPerceptronNet_ForForecast()
        elif modelType == 'RS':
            modelObj = NNBuilder.buildRnnNet_ForSummary()
        elif modelType == 'RF':
            modelObj = NNBuilder.buildRnnNet()
        elif modelType == 'AS':
            modelObj = NNBuilder.buildAutoencoder_ForSummary()
        else:
            modelObj = NNBuilder.buildAutoencoder_ForForecast()
        modelObj.fit(data['train_values'], data['train_labels'], epochs=10)
        predictResult = modelObj.predict(data['test_values'], verbose=1)
        decoded = []
        if task == 'S':
            decoded = MainMenu.SummaryModel._decode(predictResult)
        else:
            decoded = MainMenu.ForecastModel.decode(predictResult)
        print('\n train_values: {} \n train_labels: {} \n test_values: {} \n test_labels: {} \n prediction: {} \n decoded: {} \n'.format(data['train_values'][0], data['train_labels'][0], data['test_values'][0], data['test_labels'][0], predictResult[0], decoded[0]))
        # ///////////////////////////////////////////////////
        test_result = ''
        prec = Precision()
        prec.update_state(data['test_labels'], predictResult)
        test_result = test_result + ' Precision: {} '.format(prec.result().numpy())
        print(test_result)
        # if task == 'S':
        #     MainMenu.SummaryModel._neuralNetObject = modelObj
        #     MainMenu.SummaryModel.saveNet('newRnn')
        # else:
        #     MainMenu.ForecastModel._neuralNetObject = modelObj
        #     MainMenu.ForecastModel.saveNet('newRnn')
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
        MainMenu._save_forecast(result)

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