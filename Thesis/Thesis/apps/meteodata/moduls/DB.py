import psycopg2
from datetime import date


class DBControl():
    def __init__(self):
        self._connect()
        self._tables = ('meteodata', 'forecastmeteidata', 'meteodataanomalies')
        self._curTable = 0
        self._lastQuere = ''

# removers

    def removeMeteodata(self, id):
        self._curs.execute('DELETE from public.meteodata_meteodata WHERE id ={}'.format(str(id)))

    def removeForecast(self, id):
        self._curs.execute('DELETE from public.meteodata_forecastmeteodata WHERE id ={}'.format(str(id)))

    def removeAnomalies(self, id):
        self._curs.execute('DELETE from public.meteodata_meteodataanomalies WHERE id ={}'.format(str(id)))

# inserters

    def insertMeteodata(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        self._curs.execute("INSERT INTO public.meteodata_meteodata VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")

    def insertForecast(self, data):
        _id = int(self.getMaxId(self._tables[3]) + 1)
        self._curs.execute("INSERT INTO public.meteodata_forecastmeteodata VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")
        
    def insertAnomalies(self, data):
        _id = int(self.getMaxId(self._tables[0]) + 1)
        self._curs.execute("INSERT INTO public.meteodata_meteodataanomalies VALUES(DEFAULT," + data[0] + ", '{" + data[1] + "}', '{" + data[2] + "}', '{" + data[3] + "}')")

# updaters

    def updateMeteodata(self, data):
        self._curs.execute("UPDATE public.meteodata_meteodata SET datetime='" + data[0] + "', place=" + str(data[1]) + ", \"placeName\"" + data[2] + "', temperature=" + str(data[3]) + ", wind_way=" + str(data[4]) + ", wind_speed=" + str(data[5]) + ", air_pressure" + str(data[6]) + ", water_pressure" + str(data[7]) + ", weather='{" + data[8] + "}' WHERE id=" + str(data[0]))

    def updateForecast(self, data):
        self._curs.execute("UPDATE public.meteodata_forecastmeteodata SET datetime='" + data[0] + "', place=" + str(data[1]) + ", \"placeName\"" + data[2] + "', temperature=" + str(data[3]) + ", wind_way=" + str(data[4]) + ", wind_speed=" + str(data[5]) + ", air_pressure" + str(data[6]) + ", water_pressure" + str(data[7]) + ", weather='{" + data[8] + "}' WHERE id=" + str(data[0]))

    def updateAnomalies(self, data):
        self._curs.execute("UPDATE public.meteodata_meteodataanomalies SET meteodata_id=" + str(data[1]) + ", fieldname='{" + data[2] + "}', value='{" + data[3] + "}', anomaly='{" + data[4] + "}' WHERE id=" + str(data[0]))

# getters

    def getMeteodata(self, filter='id, datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather', where=''):
        self._curTable = 0
        tmp = 'SELECT {} FROM public.meteodata_meteodata {}'.format(filter, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getForecast(self, filter='id, datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather', where=''):
        self._curTable = 1
        tmp = 'SELECT {} FROM public.meteodata_forecastmeteodata {}'.format(filter, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getAnomalies(self, filter='id, meteodata_id, fieldname, value, anomaly', where=''):
        self._curTable = 2
        tmp = 'SELECT {} FROM public.meteodata_meteodataanomalies {}'.format(filter, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

# Additional functions

    def getTableNames(self):
        return self._tables

    def getMaxId(self, table):
        if table in self._tables:
            self._curs.execute('SELECT MAX(id) FROM public.{}'.format(table))
        elif isinstance(table, int):
            if table >= 0 and table < len(self._tables):
                self._curs.execute('SELECT MAX(id) FROM public.{}'.format(self._tables[table]))
        else:
            return 0
        records = self._curs.fetchall()
        if records[0][0] is None:
            return 1
        else:
            return int(records[0][0])

    def getHederLabels(self):
        if self._curTable == 0:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']# meteodata_meteodataanomalies
        elif self._curTable == 1:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']# payment_table 
        elif self._curTable == 2:
            return ['№', '№ метеоданных', 'Имя поля', 'Значение', 'Описание аномалии']# MeteodataTable

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

    def save(self):
        self._conn.commit()
    
    def _connect(self):
        self._conn = psycopg2.connect(dbname='Weather', user='postgres', password='12345', host='localhost')
        self._curs = self._conn.cursor()

    def __del__(self):
        self._conn.commit()
        self._curs.close()
        self._conn.close()