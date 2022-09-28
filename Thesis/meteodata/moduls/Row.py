from datetime import datetime


class Row:
    
    def __init__(self, data=0):
        self._keyLabels = {'datetime': 'Дата - Время', 
        'place': 'Код места', 'temperature': 'Температура', 
        'wind_way': 'Направление ветра', 'wind_speed': 'Скорость ветра', 
        'air_pressure': 'Давление воздуха', 'water_pressure': 'Давление воды', 
        'weather': 'Погодные явления', 'placeName': 'Место'}
        self._data = {'datetime': 0, 
        'place': 0, 'temperature': 0, 
        'wind_way': 0, 'wind_speed': 0, 
        'air_pressure': 0, 'water_pressure': 0, 
        'weather': 0, 'placeName': 'none'}
        if isinstance(data, dict):
            self.setData(data)

    
    def getKeys(self):
        return self._data.keys()

    def getKeyLabels(self, rule=''):
        l = rule.split(',')
        s = ''
        for item in l:
            s = s + self._keyLabels[item] + ' '
        return s

    def getData(self, rule=''):
        l = rule.split(',')
        s = ''
        for item in l:
            s = s + self._data[item] + ' '
        return s

    def setData(self, data):
        for key in data.keys():
            self._data[key] = data[key]

    def getDate(self):
        return self._data['datetime']

    def getPlace(self):
        return self._placeName

