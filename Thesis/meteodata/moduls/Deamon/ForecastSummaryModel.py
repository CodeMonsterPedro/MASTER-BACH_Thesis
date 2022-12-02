import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from datetime import datetime, date, time
import numpy as np
import subprocess, sys, random
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split 
import math, pickle, re
import time as ttime
import os
from ...models import Meteodata, ForecastMeteodata, NeuralNet


class ForecastSummaryModel:

    def __init__(self, model_id='1', modelName='my_fullconnect', dbName='meteodata_forecastmeteodata'):
        self._target = 'summary'
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
        self._correctWeatherDict = {}
        self._neuralNetObject = []
        self._metric = 'accuracy'
        self._loss = 'sparse_categorical_crossentropy'
        self._optimizer = 'adam'
        self._modelName = modelName
        self._dbName = dbName
        self._accurancy = 89.5
        self._epochs = 10
        self._correctWeatherDict = {}
        self._scoreResult = 0
        self._metricResult = 0
        tempWeatherList = []
        for item in self._weatherList.values():
            if item not in tempWeatherList:
                tempWeatherList.append(item)
        i = 1.0
        for item in tempWeatherList:
            self._correctWeatherDict.update({item: i})
            i = i + 1.0
        if model_id != '':
            self.loadNet(model_id)

    def __del__(self):
        tmp = subprocess.check_output('pwd', shell=True).decode().rstrip()
        subprocess.check_output("rm -rv {}/media/models/{}".format(tmp, self._modelName), shell=True)

    def loadDataSet(self, test=False):
        dataSet = 0
        if test:
            dataSet = ('datetime', 'place', 'temperature', 'wind_way', 'wind_speed', 'air_pressure', 'water_pressure', 'weather')
        else:
            dataSet = ('datetime', 'place', 'temperature', 'wind_way', 'wind_speed', 'air_pressure', 'water_pressure')
        if self._dbName == 'meteodata_forecastmeteodata':
            return ForecastMeteodata.objects.all().order_by('datetime').values_list(dataSet)
        elif self._dbName == 'meteodata_meteodata':
            return Meteodata.objects.all().order_by('datetime').values_list(dataSet)

    def loadNet(self, net_id):
        print('start load net: ', net_id)
        obj = NeuralNet.objects.get(pk=net_id)
        f = obj.file_data
        self._modelName = obj.name
        tmp = subprocess.check_output('pwd', shell=True).decode().rstrip()
        if not os.path.exists('{}/media/models/{}'.format(tmp, self._modelName)):
            subprocess.check_output("file-roller -h {}/media/{}".format(tmp, str(f)), shell=True)
        self._neuralNetObject = keras.models.load_model('{}/media/models/{}'.format(tmp, self._modelName))
        print('finish load')

    def test(self, metric='accuracy'):
        testData = self.loadDataSet(True)
        data = self._encode(testData)
        test_loss, test_acc = self._neuralNetObject.evaluate(data['test_values'],  data['test_labels'], verbose=2)#TODO add different metrics
        test_result = test_acc
        return test_result

    def predict(self, data):
        result = []
        tmpData = self.encode(data)
        for row in tmpData['values']:
            result.append(self._neuralNetObject.predict(row))
        return self.decode(result)
    
    def encode(self, data):
        values = data # TODO make good normalisation func?
        resultList = []
        for i in range(len(values)):
            tmp = []
            datetimeData = datetime.strptime(values[i][0][:-6], "%Y-%m-%d %H:%M:%S")
            d = datetimeData
            tmp.append(d.year)
            tmp.append(d.month)
            tmp.append(d.day) # 0 - date
            tmp.append(d.hour)
            tmp.append(float(values[i][1])) # 1 - place
            tmp.append(float(values[i][3])) # 3 - temperature
            tmp.append(float(values[i][4])) # 4 - wind_way
            tmp.append(float(values[i][5])) # 5 - wind_speed
            tmp.append(float(values[i][6])) # 6 - air_pressure
            tmp.append(float(values[i][7])) # 7 - water_pressure
            resultList.append(tmp)
        values = resultList
        train_values, test_values = train_test_split(values, test_size=0.20, random_state=42)
        print(self._train_values[:20], self._test_values[:20], self._train_labels[:20], self._test_labels[:20])
        d = {'values': values, 'train_values': train_values, 'test_values': test_values}
        return d

    def decode(self, data):
        val = self._correctWeatherDict.values()
        keys = self._correctWeatherDict.keys()
        resultList = []
        for row in data:
            for i in range(len(val)):
                if row == val[i]:
                    resultList.append(keys[i])
        return resultList

    def _buildPerceptron(self):
        data = self._encode(self.loadDataSet())
        self._buildPerceptronNet()

    def _startTraining(self):
        self._neuralNetObject.fit(self._train_values, self._train_labels, epochs=self._epochs)
        test_loss, test_acc = self._neuralNetObject.evaluate(self._test_values,  self._test_labels, verbose=2)
        self._accurancy = test_acc
        print('loss', test_loss)
        print('acc', test_acc)
        self._values = []
        self._labels = []
        self._train_values = []
        self._train_labels = []
        self._test_values = []
        self._test_labels = []

    def _buildPerceptronNet(self):
        self._neuralNetObject = keras.Sequential()
        self._neuralNetObject.add(keras.layers.InputLayer(input_shape=(len(self._values[0]),)))
        self._neuralNetObject.add(keras.layers.Dense(190, activation='relu'))
        self._neuralNetObject.add(keras.layers.Dense(1900, activation='relu'))
        self._neuralNetObject.add(keras.layers.Dense(190, activation='relu'))
        self._neuralNetObject.add(keras.layers.Dense(len(list(self._correctWeatherDict.keys())) + 1, activation='softmax'))
        self._neuralNetObject.compile(optimizer=self._optimizer, loss=self._loss, metrics=self._metric)
        self._neuralNetObject.summary()

    def _encode(self, data):
        values = data
        labels = []
        for i in range(len(values)):
            weather = values[i][-1]
            labels.append(weather)
            values[i].pop(len(values[i]) - 1)
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
            datetimeData = datetime.strptime(values[i][0][:-6], "%Y-%m-%d %H:%M:%S")
            d = datetimeData
            tmp.append(d.year)
            tmp.append(d.month)
            tmp.append(d.day) # 0 - date
            tmp.append(d.hour)
            tmp.append(float(values[i][1])) # 1 - place
            tmp.append(float(values[i][3])) # 3 - temperature
            tmp.append(float(values[i][4])) # 4 - wind_way
            tmp.append(float(values[i][5])) # 5 - wind_speed
            tmp.append(float(values[i][6])) # 6 - air_pressure
            tmp.append(float(values[i][7])) # 7 - water_pressure
            resultList.append(tmp)
        values = resultList
        train_values, test_values, train_labels, test_labels = train_test_split(values, labels, test_size=0.20, random_state=42)
        print(self._train_values[:20], self._test_values[:20], self._train_labels[:20], self._test_labels[:20])
        d = {'values': values, 'lables': labels, 'train_values': train_values, 'test_values': test_values, 'train_labels': train_labels, 'test_labels': test_labels}
        return d

    def _saveNet(self, name='Perceptron'):
        d = str(date.today())
        t = ttime.localtime()
        t = ttime.strftime("%M%S", t)
        fullName = '' + d + t + '--' + name
        subprocess.call('cd ' + MEDIA_ROOT + '/models & mkdir {}'.format(fullName))
        self._neuralNetObject.save(MEDIA_ROOT + '/models/{}'.format(fullName))

if __name__ == "__main__":
    s = subprocess.call('pwd')