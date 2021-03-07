import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from ..DB import DBControl
from datetime import datetime, date, time


class ForecastSummaryModel:

    def __init__(self):
        self._db = DBControl()
        self._method = []
        self._dataSet = 0
        self._weatherNames = {}
        self._importNet()

    def getForecastSummary(self):
        rawData = self._getDataSet()
        self._dataSet = self._prepareData(rawData)
        tryId = 0
        resultList = []
        for i in range(len(rawData)):
            tryId += 1
            tmp = rawData[i]
            tmp[-1] = self._predict(self._dataSet[i])
            resultList.append(tmp)
            if tryId >= 100:
                for row in resultList:
                    self._db.updateForecast(row)
                self._db.save()
                resultList.clear()
                tryId = 0

    def _getDataSet(self):
        s = "weather='{" + "0}'"
        data = self._db.getForecast(where=s)
        return data

    def _predict(self, row):
        values = self._method.predict(row)
        id = 0
        for i in range(len(values)):
            if values[id] < values[i]:
                id = i
        return self._weatherNames[id]

    def _importNet(self):
        self._method = keras.models.load_model('../../../../models/fullconnect.h5')

    def _prepareData(self, data):
        pass