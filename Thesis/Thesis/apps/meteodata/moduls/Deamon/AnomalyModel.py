import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from ..DB import DBControl
from datetime import datetime, date, time, timedelta
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import numpy as np
import math


class AnomalyModel:

    def __init__(self, modelName='autoencoder'):
        self._db = DBControl()
        self._methodEncoder = []
        self._methodDecoder = []
        self._modelName = modelName
        self._dataSet = 0
        self._anomalyPercent = 0
        self._epochs = 20
        self._importNet()

    def _getDataSet(self):
        data = self._db.getMeteodata(what='datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure', where='ORDER BY datetime')
        return data

    def _makeAccurancyTest(self, values, labels):
        test_loss, test_acc = self._method.evaluate(values,  labels, verbose=2)
        self._accurancy = test_acc

    def _convertToNormal(self, row, data, ttype=2):
        valtmp = []
        valtmp.append(float(d.year) * 10000)
        valtmp.append(float(d.month) * 100)
        valtmp.append(float(d.day)  * 100) # 0 - date
        valtmp.append(float(d.hour)  * 100)
        valtmp.append(float(values[1] * 10000)  + 30000) # 1 - place
        valtmp.append(float(values[3] * 10000) - 100) # 3 - temperature -
        valtmp.append(float(values[4]) * 10) # 4 - wind_way
        valtmp.append(float(values[5]) * 10000) # 5 - wind_speed -
        valtmp.append(float(values[6]) * 10000) # 6 - air_pressure
        valtmp.append(float(values[7]) * 10000) # 7 - water_pressure
        print(valtmp)
        return valtmp

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
        self._methodEncoder = keras.models.load_model('Thesis/Thesis/models/{}-encoder.h5'.format(self._modelName))
        self._methodDecoder = keras.models.load_model('Thesis/Thesis/models/{}-decoder.h5'.format(self._modelName))

    def _prepareData(self, data, ttype=2):
        values = data
        if ttype == 1:
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(values[1] - 30000) / 10000) # 1 - place
            valtmp.append(float(values[3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(values[4]) / 10) # 4 - wind_way
            valtmp.append(float(values[5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(values[6]) / 10000) # 6 - air_pressure
            valtmp.append(float(values[7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(d.year) / 10000)
            lebtmp.append(float(d.month) / 100)
            lebtmp.append(float(d.day)  / 100) # 0 - date
            lebtmp.append(float(d.hour)  / 100)
            lebtmp.append(float(values[1] - 30000) / 10000) # 1 - place
            lebtmp.append(float(values[3] + 100) / 10000) # 3 - temperature -
            lebtmp.append(float(values[4]) / 10) # 4 - wind_way
            lebtmp.append(float(values[5]) / 10000) # 5 - wind_speed -
            lebtmp.append(float(values[6]) / 10000) # 6 - air_pressure
            lebtmp.append(float(values[7]) / 10000) # 7 - water_pressure
            return (valtmp, lebtmp)
        else:
            valueList = []
            labelList = []
            valList = []
            for i in range(len(data)):
                valtmp = []
                lebtmp = []
                datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
                d = datetimeData
                valtmp.append(float(d.year) / 10000)
                valtmp.append(float(d.month) / 100)
                valtmp.append(float(d.day)  / 100) # 0 - date
                valtmp.append(float(d.hour)  / 100)
                valtmp.append(float(values[i][1] - 30000) / 10000) # 1 - place
                valtmp.append(float(values[i][3] + 100) / 10000) # 3 - temperature -
                valtmp.append(float(values[i][4]) / 10) # 4 - wind_way
                valtmp.append(float(values[i][5]) / 10000) # 5 - wind_speed -
                valtmp.append(float(values[i][6]) / 10000) # 6 - air_pressure
                valtmp.append(float(values[i][7]) / 10000) # 7 - water_pressure
                lebtmp.append(float(d.year) / 10000)
                lebtmp.append(float(d.month) / 100)
                lebtmp.append(float(d.day)  / 100) # 0 - date
                lebtmp.append(float(d.hour)  / 100)
                lebtmp.append(float(values[i][1] - 30000) / 10000) # 1 - place
                lebtmp.append(float(values[i][3] + 100) / 10000) # 3 - temperature -
                lebtmp.append(float(values[i][4]) / 10) # 4 - wind_way
                lebtmp.append(float(values[i][5]) / 10000) # 5 - wind_speed -
                lebtmp.append(float(values[i][6]) / 10000) # 6 - air_pressure
                lebtmp.append(float(values[i][7]) / 10000)
                valueList.append(valtmp)
                labelList.append(lebtmp)
            values = valueList
            labels = labelList
            return (values, labels)        

    def _isAnomaly(self, input, output, ttype=2):
        if ttype == 1:
            for i in range(len(input)):
                delta = (abs(input[i] - output[i]) / (input[i] / 100))
                if delta > 5:
                    return True
        else:
            tmp = []
            for j in range(len(input)):
                for i in range(len(input[j])):
                    delta = (abs(input[j][i] - output[j][i]) / (input[j][i] / 100))
                    if delta > 5:
                        tmp.append((input[j], output[j], j, i, delta))
            if len(tmp) == 0:
                return False
            else:
                return tmp
        return False

    def predict(self, data, ttype=2):
        l = []
        l2 = []
        if ttype == 1:
            tmp = self._prepareData(data, 1)
            l = self._methodEncoder.predict(tmp[0])
            l = self._methodDecoder.predict(l)
            return self._isAnomaly(tmp, l)
        else:
            for row in data:
                tmp1 = self._prepareData(row, 1)
                tmp = self._methodEncoder.predict(tmp1[0])
                tmp = self._methodDecoder.predict(tmp)
                l.append(tmp1)
                l2.append(tmp)
        return self._isAnomaly(l, l2)

    def scan(self):
        data = self._getDataSet()
        tdata = self._prepareData(data, 2)
        resultList = self.predict(tdata, 2)
        if resultList:
            for row in resultList:
                self._db.insertAnomalies()

    def filter(self, data, ttype=2):
        l = self.predict(data, ttype)
        if l and len(l) != 0:
            tmp = []
            tmp1 = data
            for row in l:
                tmp.append(row[2])
                tmp1.pop(row[2])
            return tmp1, tmp, l
        else:
            return data, []

    def trainModel(self, data):
        _values = data
        valueList = []
        labelList = []
        for i in range(len(_values) - 1):
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
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
            lebtmp.append(float(d.year) / 10000)
            lebtmp.append(float(d.month) / 100)
            lebtmp.append(float(d.day)  / 100) # 0 - date
            lebtmp.append(float(d.hour)  / 100)
            lebtmp.append(float(_values[i][1] - 30000) / 10000) # 1 - place
            lebtmp.append(float(_values[i][3] + 100) / 10000) # 3 - temperature -
            lebtmp.append(float(_values[i][4]) / 10) # 4 - wind_way
            lebtmp.append(float(_values[i][5]) / 10000) # 5 - wind_speed -
            lebtmp.append(float(_values[i][6]) / 10000) # 6 - air_pressure
            lebtmp.append(float(_values[i][7]) / 10000)
            valueList.append(valtmp)
            labelList.append(lebtmp)
        _values = valueList
        _labels = labelList
        _train_values, _test_values, _train_labels, _test_labels = train_test_split(_values, _labels, test_size=0.20, random_state=42)
        print(_train_values[:20], _test_values[:20], _train_labels[:20], _test_labels[:20])
        self._methodEncoder.fit(_train_values, _train_labels, epochs=self._epochs)
        tmp = self._methodEncoder.predict(_train_values)
        self._methodDecoder.fit(tmp, _train_values, epochs=self._epochs)
        self._saveNet(obj=self._methodEncoder)
        self._saveNet(obj=self._methodDecoder)

    def getStatistic(self):
        return self._anomalyPercent