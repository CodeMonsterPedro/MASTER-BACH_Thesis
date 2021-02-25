import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from .DB import DBControl
from datetime import datetime, date, time


class ForecastSummaryModel:

    def __init__(self):
        self._db = DBControl()
        self._method = []
        self._dataSet = 0


    def getForecastSummary(self):
        pass

    def _getDataSet(self):
        data = self._db.getForecast()
        return data

    def _predict(self, row):
        return self._method.predict(row)

    def _importNet(self):
        fileInfo = QFileDialog.getOpenFileName()
        fileName = fileInfo[0].split('.')
        self._method = keras.models.load_model(fileInfo[0])