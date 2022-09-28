import psycopg2
from datetime import date, datetime
import sqlite3


def refactorRecords(records):
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
            elif isinstance(element, tuple):
                result_row.append(element[0])
            elif isinstance(element, int):
                result_row.append(element)
            elif isinstance(element, float):
                result_row.append(float(element))
        result.append(result_row)
    return result

conn_post = psycopg2.connect(dbname='Weather', user='postgres', password='12345', host='localhost')
curs_post = conn_post.cursor()
print('post connected')
conn_lite = sqlite3.connect('/home/max/Projects/BACH_Thesis/Thesis/Thesis/apps/meteodata/moduls/weather.db')
curs_lite = conn_lite.cursor()
print('lite connected')
#tables = ['meteodata', 'meteodata_meteodata', 'meteodata_forecastmeteodata', 'meteodata_clearmeteodata', 'meteodata_clearforecastmeteodata', 'meteodata_meteodataanomalies']
tables = []
curs_lite.execute("SELECT name FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY 1")
tables = refactorRecords([curs_lite.fetchall(), ])
tables = tables[0]
filter='id, datetime, place, \"placeName\", temperature, wind_way, wind_speed, air_pressure, water_pressure, weather'
filter1='id, meteodata_id, fieldname, value, anomaly'
data = []
tmp = ''
for table in tables:
    print('table: ', table)
    if table != 'meteodata_meteodataanomalies':
        continue
    if table == 'meteodata_meteodataanomalies':
        tmp = 'SELECT {} FROM public.{} ORDER BY id'.format(filter1, table)
    else:
        tmp = 'SELECT {} FROM public.{} ORDER BY id'.format(filter, table)
    curs_post.execute(tmp)
    data = refactorRecords(curs_post.fetchall())
    print('get rows count: ', len(data))
    if table == 'meteodata_meteodataanomalies':
        for row in data:
            print('row id: ', row[0])
            tmp = "INSERT INTO meteodata_meteodataanomalies VALUES(" + str(row[0]) + ', ' + str(row[1]) + ", '{" + str(row[2]) + "}', '{" + str(row[3]) + "}', '{" + str(row[4]) + "}')"
            curs_lite.execute(tmp)
    else:
        for row in data:
            print('row id: ', row[0])
            tmp = "INSERT INTO " + table + " VALUES(" + str(row[0]) + ", '" + str(row[1]) + "', " + str(row[2]) + ", '" + str(row[3]) + "', " + str(row[4]) + ", " + str(row[5]) + ", " + str(row[6]) + ", " + str(row[7]) + ", " + str(row[8]) + ", '{" + str(row[9]) + "}')"
            print(tmp)
            curs_lite.execute(tmp)
    conn_lite.commit()
print('lite end')
curs_lite.close()
conn_lite.close()
print('post end')   

