import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from ..DB import DBControl
from datetime import datetime, date, time, timedelta
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import numpy as np


class SimpleForecastModel:

    def __init__(self, modelName='rnn'):
        self._db = DBControl()
        self._method = []
        self._modelName = modelName
        self._dataSet = 0
        self._accurancy = 89.5
        self._epochs = 20
        self._methodId = 2
        self._importNet()

    def _getDataSet(self):
        data = self._db.getMeteodata(what='datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure', where='ORDER BY datetime')
        return data

    def _makeAccurancyTest(self, values, labels):
        test_loss, test_acc = self._method.evaluate(values,  labels, verbose=2)
        self._accurancy = test_acc
    
    def _saveNet(self, obj, name=''):
        ttype = self._modelName
        if name == name:
            obj.save('Thesis/Thesis/models/' + ttype + "-" + name + ".h5")
        else:
            n = str(date.today())
            t = ttime.localtime()
            t = ttime.strftime("%M%S", t)
            obj.save('Thesis/Thesis/models/' + n + t + ttype + ".h5")

    def _importNet(self):
        self._method = keras.models.load_model('../../../../models/{}.h5'.format(self._modelName))

    def _convertToNormal(self, row, data):
        valtmp = []
        valtmp.append(row[0])
        valtmp.append(row[1])
        valtmp.append(row[2])
        valtmp.append(float(data[3] * 10000) - 100) # 3 - temperature -
        valtmp.append(float(data[4]) * 10) # 4 - wind_way
        valtmp.append(float(data[5]) * 10000) # 5 - wind_speed -
        valtmp.append(float(data[6]) * 10000) # 6 - air_pressure
        valtmp.append(float(data[7]) * 10000) # 7 - water_pressure
        print(valtmp)
        return valtmp

    def _prepareData(self, data):
        valtmp = []
        if len(data) == 1:
            datetimeData = datetime.strptime(data[0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(data[1] - 30000) / 10000) # 1 - place
            valtmp.append(float(data[3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(data[4]) / 10) # 4 - wind_way
            valtmp.append(float(data[5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(data[6]) / 10000) # 6 - air_pressure
            valtmp.append(float(data[7]) / 10000) # 7 - water_pressure
            return valtmp
        else:
            valList = []
            for i in range(len(data)):
                valtmp = []
                datetimeData = datetime.strptime(data[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
                d = datetimeData
                valtmp.append(float(d.year) / 10000)
                valtmp.append(float(d.month) / 100)
                valtmp.append(float(d.day)  / 100) # 0 - date
                valtmp.append(float(d.hour)  / 100)
                valtmp.append(float(data[i][1] - 30000) / 10000) # 1 - place
                valtmp.append(float(data[i][3] + 100) / 10000) # 3 - temperature -
                valtmp.append(float(data[i][4]) / 10) # 4 - wind_way
                valtmp.append(float(data[i][5]) / 10000) # 5 - wind_speed -
                valtmp.append(float(data[i][6]) / 10000) # 6 - air_pressure
                valtmp.append(float(data[i][7]) / 10000) # 7 - water_pressure
                valList.append(valtmp)
            return valList

    def update(self):
        rawData = self._getDataSet()
        self._dataSet = self._prepareData(rawData)
        resultList = []
        swhat = "DISTINCT place"
        cities = self._db.getMeteodata(s)
        for i in range(len(cities)):
            tmp = [rawData[i]]
            startDate = datetime.strptime(tmp[0][0], "%Y-%m-%d %H:%M:%S")
            place = tmp[0][1]
            placeName = tmp[0][2]
            for i in ramge((7*24) / 3):
                data = self._predict(tmp[-1])
                tmp.append(data)
                self._db.insertForecast([startDate + timedelta(hours=3), place, placeName, data[0], data[1], data[2], data[3], data[4], ])
        self._db.save()

    def predict(self, data):
        l = []
        if len(data) == 1:
            tmp = self._prepareData(data)
            l = self._method.predict(tmp)
        else:
            for row in data:
                tmp = self._prepareData(row)
                l.append(self._method.predict(tmp))
        return self._convertToNormal(row, l)

    def trainModel(self, data):
        _values = data
        valueList = []
        labelList = []
        for i in range(len(_values) - 1):
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(_values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(_values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(_values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(_values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(_values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(_values[i][6]) / 10000) # 6 - air_pressure
            valtmp.append(float(_values[i][7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(_values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(_values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(_values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(_values[i + 1][6]) / 10000)# 6 - air_pressure
            lebtmp.append(float(_values[i + 1][7]) / 10000)# 7 - water_pressure
            valueList.append(valtmp)
            labelList.append(lebtmp)
        _values = valueList
        _labels = labelList
        _train_values, _test_values, _train_labels, _test_labels = train_test_split(_values, _labels, test_size=0.20, random_state=42)
        print(_train_values[:20], _test_values[:20], _train_labels[:20], _test_labels[:20])
        self._method.fit(_train_values, _train_labels, epochs=self._epochs)
        self._saveNet(obj=self._method)
        self._makeAccurancyTest(_test_values, _test_labels)

    def getStatistic(self):
        return self._accurancy