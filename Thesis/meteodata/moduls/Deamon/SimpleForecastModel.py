import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from datetime import datetime, date, time
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import time as ttime
from ...models import Meteodata, ForecastMeteodata, NeuralNet
from tensorflow.keras.metrics import Accuracy, MeanAbsoluteError, Precision, Recall
from .NNBase import NNBase


class SimpleForecastModel(NNBase):

    def __init__(self, model_id='4', modelName='my_rnn', dbName='meteodata_meteodata'):
        NNBase.__init__(self, model_id=model_id, modelName=modelName, dbName=dbName)

    def predict(self, data):
        result = []
        tmpData = self.encode(data)
        result = self._neuralNetObject.predict(tmpData, verbose=1)
        return self.decode(result)

    def encode(self, data):
        resultList = []
        for i in range(len(data)):
            tmp = []
            d = data[i]['datetime']
            tmp.append(float(d.year))
            tmp.append(float(d.month))
            tmp.append(float(d.day)) # 0 - date
            tmp.append(float(d.hour))
            tmp.append(float(data[i]['place'])) # 1 - place
            tmp.append(float(data[i]['temperature'])) # 3 - temperature
            tmp.append(float(data[i]['wind_way'])) # 4 - wind_way
            tmp.append(float(data[i]['wind_speed'])) # 5 - wind_speed
            tmp.append(float(data[i]['air_pressure'])) # 6 - air_pressure
            tmp.append(float(data[i]['water_pressure'])) # 7 - water_pressure
            resultList.append(tmp)
        return resultList

    def _encode(self, data):
        values = data
        valueList = []
        labelList = []
        for i in range(len(values) - 1):
            valtmp = []
            lebtmp = []
            d = values[i]['datetime']
            valtmp.append(float(d.year))
            valtmp.append(float(d.month))
            valtmp.append(float(d.day)) # 0 - date
            valtmp.append(float(d.hour))
            valtmp.append(float(values[i]['place'])) # 1 - place
            valtmp.append(float(values[i]['temperature']) + 700) # 3 - temperature -
            valtmp.append(float(values[i]['wind_way']) + 700 ) # 4 - wind_way
            valtmp.append(float(values[i]['wind_speed']) + 700 ) # 5 - wind_speed -
            valtmp.append(float(values[i]['air_pressure'])) # 6 - air_pressure
            valtmp.append(float(values[i]['water_pressure'])) # 7 - water_pressure
            lebtmp.append(float(values[i + 1]['temperature']) + 700)# 3 - temperature
            lebtmp.append(float(values[i + 1]['wind_way']) + 700)# 4 - wind_way
            lebtmp.append(float(values[i + 1]['wind_speed']) + 700)# 5 - wind_speed
            lebtmp.append(float(values[i + 1]['air_pressure']))# 6 - air_pressure
            lebtmp.append(float(values[i + 1]['water_pressure']))# 7 - water_pressure
            valueList.append(valtmp)
            labelList.append(lebtmp)
        train_values, test_values, train_labels, test_labels = train_test_split(valueList, labelList, test_size=0.20)
        d = {'values': valueList, 'lables': labelList, 'train_values': train_values, 'test_values': test_values, 'train_labels': train_labels, 'test_labels': test_labels}
        return d

    def decode(self, data):
        valueList = []
        for i in range(len(data)):
            valtmp = {
                'temperature': float(f'{(data[i][0] - 700):.1f}'),
                'wind_way': int(data[i][1] - 700),
                'wind_speed': abs(float(f'{(data[i][2] - 700):.1f}')),
                'air_pressure': float(f'{data[i][3]:.1f}'),
                'water_pressure': float(f'{data[i][4]:.1f}')
            }
            valueList.append(valtmp)
        print(valueList[:10])
        return valueList

    def test(self):
        testData = self._encode(self.loadDataSet())
        predictResult = self._neuralNetObject.predict(testData['test_values'], verbose=1)
        test_result = ''
        acc = Accuracy()
        acc.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' Accuracy: {} '.format(float(f'{acc.result().numpy():.2f}'))
        prec = Precision()
        prec.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' Precision: {} '.format(float(f'{prec.result().numpy():.2f}'))
        mae = MeanAbsoluteError()
        mae.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' MeanAbsoluteError: {} '.format(float(f'{mae.result().numpy():.2f}'))
        rec = Recall()
        rec.update_state(testData['test_labels'], predictResult)# "Recall" config: '"top_k": 1'
        test_result = test_result + ' Recall: {} '.format(float(f'{rec.result().numpy():.2f}'))
        return test_result

        