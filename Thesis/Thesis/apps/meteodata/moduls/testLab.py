import sys
import random
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
import psycopg2
import math
from datetime import datetime, date, time
import time as ttime
import pickle
import re
import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString


class AnomalyDetector(Model):

    def __init__(self, values_size, latent_dim):
        super(AnomalyDetector, self).__init__()
        self.encoder = tf.keras.Sequential()
        self.encoder.add(keras.layers.InputLayer(input_shape=(values_size, )))
        self.encoder.add(keras.layers.Dense(latent_dim, activation="relu"))
        self.encoder.add(keras.layers.Dense(int(latent_dim / 2), activation="relu"))
        self.decoder = tf.keras.Sequential()
        self.decoder.add(keras.layers.InputLayer(input_shape=(int(latent_dim / 2), )))
        self.decoder.add(keras.layers.Dense(int(latent_dim / 2), activation="relu"))
        self.decoder.add(keras.layers.Dense(values_size, activation="relu"))

    def call(self, x):
        print(len(x))
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    '''
    def updateTheshold(self, data):
        reconstructions = self.predict(data)
        train_loss = tf.keras.losses.mae(reconstructions, data)
        threshold = np.mean(train_loss) + np.std(train_loss)
        print("Threshold: ", threshold)

    def predict(self, data, threshold):
        reconstructions = model(data)
        loss = tf.keras.losses.mae(reconstructions, data)
        return tf.math.less(loss, threshold)


    def isAnomaly(self, x):
        pass

    '''


class Base:

    def __init__(self):
        print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        # base struct
        self._conn = psycopg2.connect(dbname='Weather', user='postgres', password='12345', host='localhost')
        self._curs = self._conn.cursor()
        self._methodId = 0
        self._method = []
        self._metric = 'accuracy'
        self._loss = 'sparse_categorical_crossentropy'
        self._optimizer = 'adam'
        self._anomaly = []
        self._weatherList = {
            "Туман ослабел (небо видно)": "Туман","сплошной туман с осаждением изморози": "Туман","туман усиливается, небо видно": "Туман",
            "Туман без изменений (небо не видно)": "Туман","Туман начался (усилился). Небо не видно": "Туман",
            "туман": "Туман",
            "туман местами": "Туман",
            "Поземные туманы сплошным слоем (высота меньше 2 м от поверхности земли)": "Туман",
            "Туман без изменений (небо видно)": "Туман",
            "туман ослабевает, небо видно": "Туман",
            "Туман (с отложением изморози). Небо видно": "Туман",
            "поземный туман клочками": "Туман",
            "туман без изменений, небо не видно": "Туман",
            "Туман (видимость менее 1 км)": "Туман",
            "Туман ослабел (небо не видно)": "Туман",
            "Туман (с отложением изморози). Небо не видно": "Туман",
            "Туман начался (усилился). Небо видно": "Туман",
            "туман ослабевает, неба не видно": "Туман",
            "просвечивающий туман с осаждением изморози": "Туман",
            "туман на расстоянии": "Туман",
            "поземный туман сплошной": "Туман",
            "туман усиливается, небо не видно": "Туман",
            "В окрестности станции местами туман": "Туман",
            "туман без изменений, небо видно": "Туман",
            "Ливневой снег слабый": "Снег","Снег умеренный с перерывами": "Снег","Снег слабый с перерывами": "Снег","снег умеренный непрерывный": "Снег",
            "Снежная крупа (возможно с дождем) умеренная или сильная": "Мелкий снег",
            "ледяная или снежная крупа слабая": "Мелкий снег",
            "Осадки (достигают поверхности земли вдали от станции (> 5 км))": "Мелкий снег",
            "осадки в поле зрения, не достигающие земли": "Мелкий снег",
            "осадки, достигающие земли, выпадающие на расстоянии более 5 км от станции": "Мелкий снег",
            "снег умеренный с перерывами": "Снег","снег сильный непрерывный": "Снег",
            "Снег умеренный непрерывный": "Снег",
            "снег сильный с перерывами": "Снег","ливневый снег слабый": "Снег","снег": "Снег","снежные кристаллы": "Снег",
            "снежные зерна": "Снег","Снег слабый непрерывный": "Снег","Снег сильный непрерывный": "Снег",
            "ливневый снег умеренный или сильный": "Снег","Морось (незамерзающая). Снежные зерна": "Снег","Снег (возможно с туманом). Ледяные иглы": "Снег",
            "ледяные иглы": "Снег","снег слабый с перерывами": "Снег", "морось или снежные зерна": "Снег",
            "Ливневой снег умеренный или сильный": "Снег",
            "Снег (возможно с туманом). Снежные зерна": "Снег",
            "снег слабый непрерывный": "Снег","Снежная крупа (возможно с дождем) слабая": "Снег",
            "ледяная или снежная крупа умеренная или сильная": "Снег","Снег сильный с перерывами": "Снег","Снег": "Снег",
            "Поземок сильный": "Поземок","пыльный или песчаный поземок в срок или в последний час": "Поземок",
            "слабый или умеренный поземок": "Поземок",
            "сильный поземок": "Поземок",
            "Поземок (слабый или умеренный)": "Поземок",
            "Поземные туманы клочками, полосами(высота меньше 2 м от поверхности земли)": "Поземок",
            "Гроза, дождь умеренный или сильный": "Гроза", "гроза в последний час, снег с дождем или крупа слабые в последний час": "Гроза",
            "Гроза слабая или умеренная  (возможен град)": "Гроза","гроза в последний час, снег с дождем или крупа умеренные или сильные в последний час": "Гроза",
            "Гроза слабая или умеренная (возможен дождь или снег)": "Гроза слабая",
            "сильная буря усиливается": "Гроза", "слабая или умеренная буря усиливается": "Гроза",
            "Гроза слабая или умеренная (возможен град)": "Гроза",
            "гроза в срок с песчаной или пыльной бурей": "Гроза",
            "Гроза, но без осадков": "Гроза","Гроза, дождь слабый": "Гроза",
            "Пыльная (песчаная) буря, слабая или умеренная, ослабела": "",
            "Гроза, снег или град, умеренные или сильные": "Гроза","Осадки (не достигают поверхности земли)": "",
            "гроза сильная в срок с градом или крупой": "Гроза","Гроза слабая или умеренная  (возможен дождь или снег)": "Гроза",
            "Гроза сильная (возможен дождь или снег)": "Гроза","Гроза": "Гроза",
            "гроза слабая или умеренная в срок с дождем или снегом": "Гроза",
            "слабая или умеренная буря ослабевает": "Гроза","Гроза сильная (возможен град)": "Гроза",
            "гроза в последний час, дождь умеренный или сильный в срок": "Гроза",
            "гроза без осадков на станции или в поле зрения": "Гроза",
            "Гроза слабая или умеренная   (возможен дождь или снег)": "Гроза",
            "гроза слабая или умеренная в срок с градом или крупой": "Гроза",
            "гроза сильная в срок с дождем или снегом": "Гроза",
            "Гроза слабая или умеренная (возможен дождь)": "Гроза","сильная буря без изменений": "Гроза",
            "слабая или умеренная буря без изменений": "Гроза",
            "Гроза, дождь со снегом слабые": "Гроза","гроза с осадками или без них": "Гроза",
            "град умеренный или сильный": "Град","Град": "Град",
            "осадки, достигающие земли, выпадающие на расстоянии менее 5 км от станции, но не на самой станции": "Дождь",
            "Ливневый дождь со снегом": "Дождь со снегом","Морось (незамерзающая) Снежные зерна": "Мелкий дождь",
            "Дождь со снегом (ледяной дождь)": "Дождь со снегом",
            "Морось (незамерзающая) слабая с перерывами": "Мелкий дождь","морось слабая непрерывная": "Мелкий дождь",
            "дождь слабый непрерывный": "Мелкий дождь",
            "морось умеренная непрерывная": "Мелкий дождь",
            "Морось замерзающая, образующая гололёд, умеренная или сильная": "Мелкий дождь",
            "гроза в последний час, дождь слабый в срок наблюдения": "Мелкий дождь",
            "морось умеренная с перерывами": "Мелкий дождь",
            "Морось с дождем слабая": "Мелкий дождь",
            "Морось (незамерзающая) умеренная непрерывная": "Мелкий дождь",
            "морось умеренная или сильная с дождем": "Мелкий дождь",
            "морось слабая с дождем": "Мелкий дождь",
            "Морось (незамерзающая) умеренная с перерывами": "Мелкий дождь",
            "Осадки (достигают поверхности земли)": "Мелкий дождь",
            "Морось с дождем сильная или умеренная": "Мелкий дождь",
            "Морось замерзающая, образующая гололёд, слабая": "Мелкий дождь",
            "Морось (незамерзающая) сильная непрерывная": "Мелкий дождь",
            "морось слабая замерзающая": "Мелкий дождь",
            "морось сильная непрерывная": "Мелкий дождь",
            "Морось (незамерзающая) слабая непрерывная": "Мелкий дождь",
            "морось сильная с перерывами": "Мелкий дождь",
            "морось умеренная или сильная замерзающая": "Мелкий дождь",
            "дождь или морось со снегом  умеренные или сильные": "Мелкий дождь",
            "морось слабая с перерывами": "Мелкий дождь",
            "дождь сильный с перерывами": "Дождь","дождь слабый с перерывами": "Дождь",
            "Дождь (незамерзающий) сильный с перерывами": "Дождь","дождь умеренный непрерывный": "Дождь",
            "Дождь (незамерзающий) слабый непрерывный": "Дождь","Морось, дождь (замерзающие, образующие гололед)": "Дождь",
            "дождь сильный непрерывный": "Дождь","дождь умеренный или сильный замерзающий": "Дождь",
            "ледяной дождь": "Дождь","замерзающая морось или дождь": "Дождь","Ледяной дождь": "Дождь",
            "дождь слабая замерзающий": "Дождь","ливневый дождь слабый": "Дождь",
            "дождь умеренный с перерывами": "Дождь",
            "Дождь (незамерзающий) слабый с перерывами": "Дождь","Дождь (незамерзающий) сильный непрерывный": "Дождь","Дождь (незамерзающий) умеренный непрерывный": "Дождь",
            "Дождь (незамерзающий) умеренный с перерывами": "Дождь",
            "Морось (незамерзающая) сильная с перерывами": "Дождь",
            "Дождь (незамерзающий)": "Дождь","дождь": "Дождь","Дождь замерзающий, образующий гололёд, умеренный или сильный": "Дождь",
            "дождь слабый замерзающий": "Дождь","Дождь замерзающий, образующий гололёд, слабый": "Дождь",
            "дождь или морось со снегом слабые": "Дождь","Ливневой дождь слабый": "Ливневой дождь",
            "ливневый снег или ливневый снег с дождем": "Дождь со снегом",
            "Дождь со снегом слабый": "Дождь со снегом",
            "Ливневой дождь со снегом слабый": "Дождь со снегом",
            "ливневый дождь со снегом, слабый": "Дождь со снегом",
            "дождь со снегом": "Дождь со снегом",
            "Дождь со снегом (умеренный или сильный)": "Дождь со снегом",
            "Ливневой дождь со снегом умеренный или сильный": "Дождь со снегом",
            "Ливневой дождь умеренный или сильный": "Ливневой дождь",
            "ливневый дождь со снегом, умеренный или сильный": "Ливневой дождь",
            "ливневый дождь умеренный или сильный": "Ливневой дождь",
            "Ливневой дождь очень сильный": "Ливневой дождь",
            "Ливневый дождь": "Ливневой дождь",
            "ливневый дождь": "Ливневой дождь",
            "ливневый дождь очень сильный": "Ливневой дождь",
            "Град (возможно с дождем)  слабый": "Град",
            "град слабый": "Град",
            "град или крупа": "Град",
            "пыль, поднятая на станции или вблизи станции": "Пыльная буря",
            "Пыльная (песчаная) буря, слабая или умеренная": "Пыльная буря",
            "Пыль, песок или брызги, поднятые ветром": "Пыльная буря",
            "пыль, принесенная издалека": "Пыльная буря",
            "Пыль, взвешенная в воздухе в обширном пространстве, но не поднятая ветром": "Пыльная буря",
            "Пыльная/песчаная буря": "Пыльная буря",
            "Пыльные/песчаные сильные вихри, но пыльной/песчаной бури нет": "Пыльная буря",
            "Пыльная или песчаная буря (с осадками или без них)": "Пыльная буря",
            "пыльные или песчаные вихри": "Пыльная буря",
            "Пыльная или песчаная буря (сильная) ослабела": "Пыльная буря",
            "дымка": "Дымка",
            "мгла": "Дымка",
            "видимость ухудшена из-за дыма": "Дымка",
            "Мгла": "Дымка",
            "Ухудшение видимости из-за дыма или вулканического пепла": "Дымка",
            "Дымка (видимость больше 1 км)": "Дымка",
            "Шквал": "Шквал",
            "шквал на станции или в поле зрения": "Шквал",
            "смерч на станции или в поле зрения": "Смерч",
            "облака рассеиваются": "Нет",
            "небо без изменений": "Нет",
            "Количество облаков не изменилось": "Нет",
            "В окрестности станции тумана нет": "Нет",
            "Количество облаков увеличилось": "Нет","Количество облаков уменьшилось": "Нет",
            "облака развиваются": "Нет",
            "наблюдения над развитием облаков не было": "Нет",
            "//": "Нет",
            "Изменение количества облаков неизвестно": "Нет",
            "Метель низовая (слабая или умеренная)": "Метель",
            "Метель низовая сильная": "Метель",
            "сильная низовая метель": "Метель",
            "слабая или умеренная низовая метель": "Метель",
            "зарница": "Зарница",
            "Зарница": "Зарница",
        }
        # data
        self._epochs = 10
        self._dataSet = []
        self._values = []
        self._labels = []
        self._train_values = []
        self._train_labels = []
        self._test_values = []
        self._test_labels = []
        self._predictions = []
        self._correctWeatherDict = {}
        # results
        self._scoreResult = 0
        self._metricResult = 0
        self._isFileParsed = False
        self._isModelUploaded = False
    
    def predictValues(self, dataSet):
        result = [[0], [1], 3]
        if self._methodId == 1:
            for item in dataSet:
                result[0].append(item[0])
                result[1].append(item[1])
            result[2] = self._method.predict(dataSet)
        return result

    def _startTraining(self):
        self._method.fit(self._train_values, self._train_labels, epochs=self._epochs)
        if self._methodId in [1, 2]:
            self._saveNet(obj=self._method)
        elif self._methodId == 0:
            self._saveNet(obj=self._method.encoder, name='encoder')
            self._saveNet(obj=self._method.decoder, name='decoder')
        test_loss, test_acc = self._method.evaluate(self._test_values,  self._test_labels, verbose=2)
        self._predictions = self._method.predict(self._test_values)
        print(self._predictions) 
        print('loss', test_loss)
        print('acc', test_acc)

    def buildAutoencoder(self):
        data = self._getStartData()# self._train_values, self._train_labels, self._test_values,  self._test_labels, self._values, self._labels
        self._getWeatherList()
        self._buildDataForAutoencoder(data)
        self._buildAutoencoderNet()

    def buildPerceptron(self):
        data = self._getStartData()
        self._getWeatherList()
        self._buildDataForPerceptron(data)
        self._buildPerceptronNet()
    
    def buildRnn(self):
        data = self._getStartData()
        self._getWeatherList()
        self._buildDataForRnn(data)
        self._buildRnnNet()

    def _buildAutoencoderNet(self):
        self._method = keras.Sequential()
        self._loss = 'mean_squared_error'
        self._method = AnomalyDetector(len(self._values[0]), 100)
        self._method.compile(optimizer=self._optimizer, loss=self._loss, metrics=self._metric)
        #self._method.summary()
    
    def _buildPerceptronNet(self):
        self._method = keras.Sequential()
        self._method.add(keras.layers.InputLayer(input_shape=(len(self._values[0]),)))
        self._method.add(keras.layers.Dense(190, activation='relu'))
        self._method.add(keras.layers.Dense(1900, activation='relu'))
        self._method.add(keras.layers.Dense(190, activation='relu'))
        self._method.add(keras.layers.Dense(len(list(self._correctWeatherDict.keys())) + 1, activation='softmax'))
        self._method.compile(optimizer=self._optimizer, loss=self._loss, metrics=self._metric)
        self._method.summary()

    def _buildRnnNet(self):
        self._method = []
        #self._metric = 'mean_absolute_error'
        self._loss = 'mean_squared_error'
        self._method = keras.Sequential()
        self._method.add(keras.layers.Embedding(input_dim=len(self._values[0]), output_dim=len(self._labels[0])))
        self._method.add(keras.layers.LSTM(128))
        self._method.add(keras.layers.Dense(len(self._labels[0]), activation='softmax'))
        self._method.compile(optimizer=self._optimizer, loss=self._loss, metrics=self._metric)
        self._method.summary()


    def _buildDataForAutoencoder(self, data):
        self._values = data
        valueList = []
        labelList = []
        for i in range(len(self._values) - 1):
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 10000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(d.year) / 10000)
            lebtmp.append(float(d.month) / 100)
            lebtmp.append(float(d.day)  / 100) # 0 - date
            lebtmp.append(float(d.hour)  / 100)
            lebtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            lebtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            lebtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            lebtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            lebtmp.append(float(self._values[i][6]) / 10000) # 6 - air_pressure
            lebtmp.append(float(self._values[i][7]) / 10000) # 7 - water_pressure
            '''
            last one
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 1000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 1000) # 7 - water_pressure
            lebtmp.append(float(self._values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(self._values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(self._values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(self._values[i + 1][6]) / 1000)# 6 - air_pressure
            lebtmp.append(float(self._values[i + 1][7]) / 1000)# 7 - water_pressure

            best one
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 10000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(self._values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(self._values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(self._values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(self._values[i + 1][6]) / 10000)# 6 - air_pressure
            lebtmp.append(float(self._values[i + 1][7]) / 10000)# 7 - water_pressure
            '''
            valueList.append(valtmp)
            labelList.append(lebtmp)
        self._values = valueList
        self._labels = labelList
        self._train_values, self._test_values, self._train_labels, self._test_labels = train_test_split(self._values, self._labels, test_size=0.20, random_state=42)
        print(self._train_values[:20], self._test_values[:20], self._train_labels[:20], self._test_labels[:20])

    def _buildDataForPerceptron(self, data):
        self._values = data
        for i in range(len(self._values)):
            weather = self._values[i][-1]
            self._labels.append(weather)
            self._values[i].pop(len(self._values[i]) - 1)
        for i in range(len(self._labels)):
            try:
                temp = self._labels[i]
                if temp.isdigit():
                    self._labels[i] = "Нет"
                else:
                    self._labels[i] = self._weatherList[self._labels[i]]
            except:
                self._labels[i] = "Нет"
        for i in range(len(self._labels)):
            self._labels[i] = (self._correctWeatherDict[self._labels[i]])
        resultList = []
        for i in range(len(self._values)):
            tmp = []
            datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            tmp.append(d.year)
            tmp.append(d.month)
            tmp.append(d.day) # 0 - date
            tmp.append(d.hour)
            tmp.append(float(self._values[i][1])) # 1 - place
            tmp.append(float(self._values[i][3])) # 3 - temperature
            tmp.append(float(self._values[i][4])) # 4 - wind_way
            tmp.append(float(self._values[i][5])) # 5 - wind_speed
            tmp.append(float(self._values[i][6])) # 6 - air_pressure
            tmp.append(float(self._values[i][7])) # 7 - water_pressure
            resultList.append(tmp)
        self._values = resultList
        self._train_values, self._test_values, self._train_labels, self._test_labels = train_test_split(self._values, self._labels, test_size=0.20, random_state=42)
        print(self._train_values[:20], self._test_values[:20], self._train_labels[:20], self._test_labels[:20])

    def _buildDataForRnn(self, data):
        self._values = data
        valueList = []
        labelList = []
        for i in range(len(self._values) - 1):
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(self._values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
            d = datetimeData
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 10000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(self._values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(self._values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(self._values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(self._values[i + 1][6]) / 10000)# 6 - air_pressure
            lebtmp.append(float(self._values[i + 1][7]) / 10000)# 7 - water_pressure
            '''
            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 1000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 1000) # 7 - water_pressure
            lebtmp.append(float(self._values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(self._values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(self._values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(self._values[i + 1][6]) / 1000)# 6 - air_pressure
            lebtmp.append(float(self._values[i + 1][7]) / 1000)# 7 - water_pressure

            valtmp.append(float(d.year) / 10000)
            valtmp.append(float(d.month) / 100)
            valtmp.append(float(d.day)  / 100) # 0 - date
            valtmp.append(float(d.hour)  / 100)
            valtmp.append(float(self._values[i][1] - 30000) / 10000) # 1 - place
            valtmp.append(float(self._values[i][3] + 100) / 10000) # 3 - temperature -
            valtmp.append(float(self._values[i][4]) / 10) # 4 - wind_way
            valtmp.append(float(self._values[i][5]) / 10000) # 5 - wind_speed -
            valtmp.append(float(self._values[i][6]) / 10000) # 6 - air_pressure
            valtmp.append(float(self._values[i][7]) / 10000) # 7 - water_pressure
            lebtmp.append(float(self._values[i + 1][3] + 100) / 10000)# 3 - temperature
            lebtmp.append(float(self._values[i + 1][4]) / 10)# 4 - wind_way
            lebtmp.append(float(self._values[i + 1][5]) / 10000)# 5 - wind_speed
            lebtmp.append(float(self._values[i + 1][6]) / 10000)# 6 - air_pressure
            lebtmp.append(float(self._values[i + 1][7]) / 10000)# 7 - water_pressure
            '''
            valueList.append(valtmp)
            labelList.append(lebtmp)
        self._values = valueList
        self._labels = labelList
        self._train_values, self._test_values, self._train_labels, self._test_labels = train_test_split(self._values, self._labels, test_size=0.20, random_state=42)
        print(self._train_values[:20], self._test_values[:20], self._train_labels[:20], self._test_labels[:20])

# -------------------------------  

# SETTERS

    def _getWeatherList(self):
        tempWeatherList = []
        for item in self._weatherList.values():
            if item not in tempWeatherList:
                tempWeatherList.append(item)
        i = 1.0
        for item in tempWeatherList:
            self._correctWeatherDict.update({item: i})
            i = i + 1.0

    def _getStartData(self):
        if self._methodId == 0:
            self._curs.execute("SELECT datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather FROM public.meteodata_meteodata")
            result = self._refactorRecords(self._curs.fetchall())
            self._curs.execute("SELECT datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather FROM public.meteodata_clearmeteodata")
            result2 = self._refactorRecords(self._curs.fetchall())
            return (result, result2)
        elif self._methodId == 1:
            self._curs.execute("SELECT datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather FROM public.meteodata_meteodata")
            result = self._refactorRecords(self._curs.fetchall())
            return result
        elif self._methodId == 2:
            self._curs.execute("SELECT datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather FROM public.meteodata_meteodata ORDER BY datetime")
            result = self._refactorRecords(self._curs.fetchall())
            return result
        else:
            return 0

    def _saveNet(self, obj, name=''):
        ttype = ""
        if self._methodId == 0:
                ttype = "Autoencoder"
        elif self._methodId == 1:
                ttype = "Perceptron"
        elif self._methodId == 2:
                ttype = "Rnn"
        if name == name:
            obj.save('Thesis/Thesis/models/' + ttype + "-" + name + ".h5")
        else:
            n = str(date.today())
            t = ttime.localtime()
            t = ttime.strftime("%M%S", t)
            obj.save('Thesis/Thesis/models/' + n + t + ttype + ".h5")

    def _importNet(self):
        fileInfo = QFileDialog.getOpenFileName()
        fileName = fileInfo[0].split('.')
        return keras.models.load_model(fileInfo[0])

# ADDITIONAL

    def _refactorRecords(self, records):
        result = list()
        for row in records:
            result_row = list()
            for element in row:
                if isinstance(element, datetime):
                    result_row.append(str(element))
                elif isinstance(element, str):
                    if element.isdigit():
                        result_row.append(float(element))
                    else:
                        if element[0] == '{':
                            result_row.append(element[1: -1])
                        else:
                            result_row.append(element)
                elif isinstance(element, list):
                    result_row.append(element[0])
                elif isinstance(element, int):
                    result_row.append(element)
                elif isinstance(element, float):
                    result_row.append(float(element))
            result.append(result_row)
        return result

    def __del__(self):
        self._conn.commit()
        self._curs.close()
        self._conn.close()

def _getSetData(name='', html='', part=0):
        items = html.find_all(attrs={'name': name})
        temp1 = []
        temp2 = []
        for child in items[part].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        return temp1, temp2

def remakeData():
    url='https://meteopost.com/weather/archive/'
    r = requests.get(url)
    html = bs(r.content, 'html.parser')
    citySet = {}
    value, text = _getSetData(name='city', html=html, part=1)
    for i in range(len(value)):
        citySet.update({value[i]: text[i]})
    _f = open('/home/max/Projects/data', 'r')
    lines = _f.readlines()
    r = re.compile('^days=[0-9](2)[\n]$')
    i = 0
    while True:
        line = lines[i]
        nextLine = lines[i+1]
        temp = str(line[-1:-9:-1])
        if temp[::-1] not in ('days=28\n', 'days=29\n', 'days=30\n', 'days=31\n'):
            #print(list(temp[::-1]))
            lines[i] = lines[i].rstrip() + nextLine
            lines.pop(i+1)
        i = i + 1
        if i + 1 == len(lines):
            break
    _f.close()
    _f = open('/home/max/Projects/data', 'w')
    _f.writelines(lines)
    i = 0
    headers = []
    AllDataList = []
    while True:
        line = lines[i]
        baseList = line.split('&&')
        if line[0] == '&':
            #print(baseList[1])
            i = i + 1
            continue
        dataList = baseList[0].split('_')
        querryList = baseList[1].split('&')
        if dataList[0] == '':
            dataList.pop(0)
        if line[:3] == '_Де':
            headers = dataList
            i = i + 1
            continue
        d = dict()
        for j in range(len(dataList)):
            if dataList[j] != '=':
                d.update({headers[j]: dataList[j]})
            else:
                d.update({headers[j]: '?'})
        for item in querryList:
            temp = item.split('=')
            d.update({temp[0]: temp[1]})
        if isinstance(d['Темп. Возд'], str):
            d['Темп. Возд'] = d['Темп. Возд'][:-1]
        if isinstance(d['Скор ветра'], str):
            d['Скор ветра'] = d['Скор ветра'].split(' ')
            d['Скор ветра'] = d['Скор ветра'][0]
        if d['День'] == '0':
            d['День'] = '26'
        xx = d['Час'].split(':')
        if int(xx[0]) > 24:
            d['Час'] = '12:00'
        AllDataList.append(d)
        i = i + 1
            #11-3
            #4-10
        if i == len(lines):
            break
    #self._curs.execute("INSERT INTO public.meteodata VALUES(DEFAULT, '" + str(d['y']) + "-" + str(d['m']) + "-" + str(d['День']) + " " + str(d['Час']) + ":00', " + str(d['city']) + ", '" + citySet[d['city']] + "', " + str(d['Темп. Возд']) + ", " + str(d['Ветер']) + ", " + str(d['Скор ветра']) + ", " + str(d['Давл станц']) + ", " + str(d['Давл моря']) + ", '{" + str(d['Явления погоды']) + "}')")
    #self._conn.commit()
    _f.close()
    checkData(AllDataList, citySet)

def checkData(data, citySet):
    _conn = psycopg2.connect(dbname='Weather', user='postgres', password='12345', host='localhost')
    _curs = _conn.cursor()
    #ErrorList = ['?', '']
    ErrorList = []
    ErrorList2 = []
    last = -1
    lastSpeed = -1
    lastTemp = -100
    fixList = []
    fixList2 = []
    for i in range(len(data)):
        d = data[i]
        if isinstance(last, int) or d['День'] != last['День']:
            if lastSpeed == -1:
                for v in fixList:
                    ErrorList.append(v)
            if lastTemp == -100:
                for v in fixList2:
                    ErrorList2.append(v)
            last = d
            lastSpeed = -1
            lastTemp = -100
            fixList = []
            fixList2 = []
        if d['Давл станц'] == '?':
            d['Давл станц'] = 760
        if d['Давл моря'] == '?' or d['Давл моря'] == '410':
            d['Давл моря'] = 760
        if d['Явления погоды'] == '?' or d['Явления погоды'] == '':
            d['Явления погоды'] = 'Нет'
        if d['Скор ветра'] == '?' and lastSpeed != -1:
            d['Скор ветра'] = lastSpeed
        elif lastSpeed != -1:
            lastSpeed = d['Скор ветра']
            if len(fixList) != 0:
                for v in fixList:
                    data[v]['Скор ветра'] = lastSpeed
        else:
            fixList.append(i)
        if d['Темп. Возд'] in ['?', '', None] and lastTemp != -100:
            d['Темп. Возд'] = lastTemp
            d['Темп. Возд'] = float(d['Темп. Возд'])
        elif lastTemp != -100:
            lastTemp = float(d['Темп. Возд'])
            if len(fixList2) != 0:
                for v in fixList2:
                    data[v]['Темп. Возд'] = lastTemp
        else:
            fixList2.append(i)
    tmp = {}
    for d in data:
        if d['m'] not in list(tmp.keys()):
            tmp.update({d['m']: [-100, ]})
        elif d['Темп. Возд'] not in ['?', '', None]:
            tmp[d['m']].append(float(d['Темп. Возд']))
    tmp2 = {}
    for key in list(tmp.keys()):
        tmp[key] = tmp[key][1:]
        print(tmp[key])
        tmp2.update({key: np.mean(tmp[key])})
    for i in ErrorList:
        data[i]['Скор ветра'] = 0
        data[i]['Темп. Возд'] = tmp2[data[i]['m']]
    for d in data:
        s = "INSERT INTO public.meteodata_meteodata VALUES(DEFAULT, '" + str(d['y']) + "-" + str(d['m']) + "-" + str(d['День']) + " " + str(d['Час']) + ":00', " + str(d['city']) + ", '" + citySet[d['city']] + "', " + str(d['Ветер']) + ", " + str(d['Скор ветра']) + ", " + str(d['Давл станц']) + ", " + str(d['Давл моря']) + ", '{" + str(d['Явления погоды']) + "}'," + str(d['Темп. Возд']) + ")"
        print(s)
        _curs.execute(s)
        _conn.commit()
    _curs.close()
    _conn.close()
    '''
    flag = True
    for d in data[1000:]:
        if d['d'] == '1' and d['m'] == '04' and d['y'] == '2011' and d['city'] == '33614' and d['arc'] == '2' and d['days'] == '30\n':
            flag = False
        if flag: 
            continue
        if d['y'] in ErrorList:
            continue
        if d['m'] in ErrorList:
            continue
        if d['День'] in ErrorList:
            continue
        if d['Час'] in ErrorList:
            continue
        if d['city'] in ErrorList:
            continue
        if d['Темп. Возд'] in ErrorList:
            continue
        if d['Ветер'] in ErrorList:
            continue
        if d['Явления погоды'] in ErrorList:
            continue
        if d['Давл станц']in ErrorList:
            continue
        if d['Давл моря'] in ErrorList:
            continue
        if d['Скор ветра'] in ErrorList:
            continue
        s = "INSERT INTO public.meteodata_clearmeteodata VALUES(DEFAULT, '" + str(d['y']) + "-" + str(d['m']) + "-" + str(d['День']) + " " + str(d['Час']) + ":00', " + str(d['city']) + ", '" + citySet[d['city']] + "', " + str(d['Темп. Возд']) + ", " + str(d['Ветер']) + ", " + str(d['Скор ветра']) + ", " + str(d['Давл станц']) + ", " + str(d['Давл моря']) + ", '{" + str(d['Явления погоды']) + "}')"
        _curs.execute(s)
        _conn.commit()
    _curs.close()
    _conn.close()
    last = -1
    lastSpeed = -1
    fixList = []
    for i in range(len(data)):
        d = data[i]
        if isinstance(last, int) or d['День'] != last['День']:
            if lastSpeed == -1:
                for v in fixList:
                    ErrorList.append(v)
            last = d
            lastSpeed = -1
            fixList = []
        if d['Давл станц'] == '?':
            d['Давл станц'] = 760
        if d['Давл моря'] == '?' or d['Давл моря'] == '410':
            d['Давл моря'] = 760
        if d['Скор ветра'] == '?':
            d['Скор ветра'] = lastSpeed
        elif lastSpeed != -1:
            lastSpeed = d['Скор ветра']
            if len(fixList) != 0:
                for v in fixList:
                    data[v]['Скор ветра'] = lastSpeed
        else:
            fixList.append(i)
    print("!kek!", data[0].keys())
    print(ErrorList)
    '''

if __name__ == "__main__":
    neural = False
    if neural:
        b = Base()
        b._methodId = 0
        test = False
        if test:
            b._importNet()
            data = b._getStartData()
            predictions = b._predict(data)
            for i in range(len(predictions)):
                print("try {}".format(i), data[i], predictions[i])
        else:
            b._epochs = 20
            if b._methodId == 1:
                b.buildPerceptron()
                b._startTraining()
            elif b._methodId == 2:
                b.buildRnn()
                b._startTraining()
            else:
                b.buildAutoencoder()
                b._startTraining()
    else:
        remakeData()
        

