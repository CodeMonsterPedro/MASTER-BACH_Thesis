import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from datetime import datetime, date, time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split 
import time as ttime
from ...models import Meteodata, ForecastMeteodata, NeuralNet
from tensorflow.keras.metrics import Accuracy, MeanSquaredError, MeanAbsoluteError, RootMeanSquaredError
from .NNBase import NNBase
 

class ForecastSummaryModel(NNBase):

    def __init__(self, model_id='3', modelName='my_fullconnect', dbName='meteodata_forecastmeteodata'):
        NNBase.__init__(self, model_id=model_id, modelName=modelName, dbName=dbName)

    def predict(self, data):
        result = []
        tmpData = self.encode(data)
        for row in tmpData:
            result.append(self._neuralNetObject.predict(row, verbose=1))
        return self.decode(result)
    
    def _predict(self, data):
        result = []
        for row in data:
            result.append(self._neuralNetObject.predict(row, verbose=1))
        return result

    def decode(self, data):
        val = list(self._correctWeatherDict.values())
        keys = list(self._correctWeatherDict.keys())
        resultList = []
        for row in data:
            maxValueIndex = 0
            if isinstance(row, float):
                maxValueIndex = row - 1
            else:
                maxValueIndex = 0
                for i in range(len(row)):
                    if row[i] > row[maxValueIndex]:
                        maxValueIndex = i
            for i in range(len(val)):
                if maxValueIndex + 1 == val[i]:
                    resultList.append(keys[i])
        return resultList
    
    def encode(self, data):
        values = data # TODO make good normalisation func?
        resultList = []
        for i in range(len(values)):
            tmp = []
            d = values[i]['datetime']
            tmp.append(d.year)
            tmp.append(d.month)
            tmp.append(d.day) # 0 - date
            tmp.append(d.hour)
            tmp.append(float(values[i]['place'])) # 1 - place
            tmp.append(float(values[i]['temperature'])) # 3 - temperature
            tmp.append(float(values[i]['wind_way'])) # 4 - wind_way
            tmp.append(float(values[i]['wind_speed'])) # 5 - wind_speed
            tmp.append(float(values[i]['air_pressure'])) # 6 - air_pressure
            tmp.append(float(values[i]['water_pressure'])) # 7 - water_pressure
            resultList.append(tmp)
        return resultList

    def _encode(self, data):
        values = data
        labels = []
        for i in range(len(values)):
            weather = values[i]['weather']
            labels.append(weather)
        for i in range(len(labels)):
            try:
                temp = labels[i]
                if temp.isdigit():
                    labels[i] = "Нет"
                else:
                    labels[i] = self._weatherList[labels[i]]
            except:
                labels[i] = "Нет"
        for i in range(len(labels)):
            labels[i] = (self._correctWeatherDict[labels[i]])
        resultList = []
        for i in range(len(values)):
            tmp = []
            d = values[i]['datetime']
            tmp.append(d.year)
            tmp.append(d.month)
            tmp.append(d.day)  # 0 - date
            tmp.append(d.hour)
            tmp.append(float(values[i]['place'])) # 1 - place
            tmp.append(float(values[i]['temperature'])) # 3 - temperature
            tmp.append(float(values[i]['wind_way'])) # 4 - wind_way
            tmp.append(float(values[i]['wind_speed'])) # 5 - wind_speed
            tmp.append(float(values[i]['air_pressure'])) # 6 - air_pressure
            tmp.append(float(values[i]['water_pressure'])) # 7 - water_pressure
            resultList.append(tmp)
        values = resultList
        train_values, test_values, train_labels, test_labels = train_test_split(values, labels, test_size=0.20, random_state=42)
        d = {'values': values, 'lables': labels, 'train_values': train_values, 'test_values': test_values, 'train_labels': train_labels, 'test_labels': test_labels}
        return d
    
    def test(self):
        for obj in self._neuralNetObject.layers:
            print(obj.get_weights()[0])
        testData = self._encode(list(Meteodata.objects.all().order_by('-datetime').values()[:500000]))
        predictResult = self._predict(testData['test_values'])
        test_result = ''
        acc = Accuracy()
        acc.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' Accuracy: {} '.format(acc.result().numpy())
        mse = MeanSquaredError()
        mse.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' MeanSquaredError: {} '.format(mse.result().numpy())
        mae = MeanAbsoluteError()
        mae.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' MeanAbsoluteError: {} '.format(mae.result().numpy())
        rmse = RootMeanSquaredError()
        rmse.update_state(testData['test_labels'], predictResult)
        test_result = test_result + ' RootMeanSquaredError: {} '.format(str(rmse.result().numpy()))
        return test_result
