import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from ..DB import DBControl
from datetime import datetime, date, time, timedelta
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import numpy as np
import math
import time as ttime


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

class AnomalyModel:

    def __init__(self, modelName='autoencoder'):
        self._db = DBControl()
        self._methodEncoder = []
        self._methodDecoder = []
        self._metric = 'accuracy'
        self._loss = 'mean_squared_error'
        self._optimizer = 'adam'
        self._modelName = modelName
        self._dbName = dbName
        self._accurancy = 89.5
        self._epochs = 10
        self._values = []
        self._labels = []
        self._train_values = []
        self._train_labels = []
        self._test_values = []
        self._test_labels = []
        self._correctWeatherDict = {}
        self._scoreResult = 0
        self._metricResult = 0
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
        tempWeatherList = []
        for item in self._weatherList.values():
            if item not in tempWeatherList:
                tempWeatherList.append(item)
        i = 1.0
        for item in tempWeatherList:
            self._correctWeatherDict.update({item: i})
            i = i + 1.0
        self.buildAutoencoder()
        self._startTraining()

    def buildAutoencoder(self):
        data = self._getDataSet()
        self._buildDataForAutoencoder(data)
        self._buildAutoencoderNet()

    def _startTraining(self):
        self._method.fit(self._train_values, self._train_labels, epochs=self._epochs)
        test_loss, test_acc = self._method.evaluate(self._test_values,  self._test_labels, verbose=2)
        print('loss', test_loss)
        print('acc', test_acc)
        self._values = []
        self._labels = []
        self._train_values = []
        self._train_labels = []
        self._test_values = []
        self._test_labels = []
        self._methodEncoder = self._method.encoder
        self._methodDecoder = self._method.decoder

    def _buildAutoencoderNet(self):
        self._method = keras.Sequential()
        self._loss = 'mean_squared_error'
        self._method = AnomalyDetector(len(self._values[0]), 100)
        self._method.compile(optimizer=self._optimizer, loss=self._loss, metrics=self._metric)

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
            valueList.append(valtmp)
            labelList.append(lebtmp)
        self._values = valueList
        self._labels = labelList
        self._train_values, self._test_values, self._train_labels, self._test_labels = train_test_split(self._values, self._labels, test_size=0.20, random_state=42)

    def _getDataSet(self):
        data = self._db.getMeteodata(filter='datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure', where='ORDER BY datetime')
        dataId = self._db.getMeteodata(filter='id', where='ORDER BY datetime')
        return data, dataId

    def _convertToNormal(self, row, data, ttype=2):
        valtmp = []
        valtmp.append(row[0])
        valtmp.append(row[1])
        valtmp.append(row[2])
        valtmp.append(float(data[1] * 10000)  + 30000) # 1 - place
        valtmp.append(float(data[3] * 10000) - 100) # 3 - temperature -
        valtmp.append(float(data[4]) * 10) # 4 - wind_way
        valtmp.append(float(data[5]) * 10000) # 5 - wind_speed -
        valtmp.append(float(data[6]) * 10000) # 6 - air_pressure
        valtmp.append(float(data[7]) * 10000) # 7 - water_pressure
        print(valtmp)
        return valtmp

    def _prepareData(self, data, ttype=2):
        print('prepareData')
        values = data
        if ttype == 1:
            valtmp = []
            lebtmp = []
            datetimeData = datetime.strptime(values[0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
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
                datetimeData = datetime.strptime(values[i][0][:-6], "%Y-%m-%d %H:%M:%S")# 0 - datetime, 1 - place, 2 - placeName, 3 - temperature, 4 - wind_way, 5 - wind_speed, 6 - air_pressure, 7 - water_pressure, 8 - weather
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
        dataNames = ['datetime', 'place', 'placeName', 'temperature', 'wind_way', 'wind_speed', 'air_pressure', 'water_pressure', 'weather']
        data, dataId = self._getDataSet()
        resultList = self.predict(data, 2)
        if resultList:
            for row in resultList:
                fieldName = dataNames[row[3]]
                self._db.insertAnomalies((dataId[row[2]], fieldName, row[0][row[3]]), 'отклонение ожидаемого значения на {}%'.format(row[4]))

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

    def getStatistic(self):
        return self._anomalyPercent