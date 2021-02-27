import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from .DB import DBControl
from datetime import datetime, date, time, timedelta


class SimpleForecastModel:

    def __init__(self):
        self._db = DBControl()
        self._method = []
        self._dataSet = 0
        self._weatherNames = {}
        self._importNet()

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

    def _getDataSet(self):
        swhat = "DISTINCT place"
        cities = self._db.getMeteodata(s)
        data = []
        for city in cities:
            swhere = "place={} ORDER BY id LIMIT 1".format(city)
            data.append(self._db.getMeteodata(what='datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure', where=swhere))
        return data

    def _predict(self, row):
        values = self._method.predict(row)
        return values

    def _importNet(self):
        self._method = keras.models.load_model('../../../models/rnn.h5')

    def _prepareData(self, data):
        pass