from datetime import datetime, timedelta
from ..models import Meteodata
from ..forms import MeteodataForm
import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from calendar import monthrange
import time
import re
from datetime import date, datetime


class MeteodataMiner:

    def __init__(self):
        self._rawData = []
        self._urls = ['https://meteopost.com/weather/archive/']

    def getLastDate(self):
        startDate = Meteodata.objects.all().order_by('-datetime').values('datetime').first()
        print(startDate)
        if startDate:
            return startDate['datetime']
        else:
            return datetime(1990, 1, 1)

    def updateMeteodata(self):
        print('meteodataminer update start')
        startDate = self.getLastDate()
        citySet, meteodata = self.startParse(startDate=startDate)
        print('meteodataminer save start')
        for row in meteodata:
            data = {
                'datetime': row['fullDate'], 
                'place': row['city'], 
                'place_name': row['cityName'], 
                'temperature': row['Темп. Возд'], 
                'wind_way': row['Ветер'], 
                'wind_speed': row['Скор ветра'], 
                'air_pressure': row['Давл станц'], 
                'water_pressure': row['Давл моря'], 
                'weather': row['Явления погоды']
            }
            form = MeteodataForm(data)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        print('meteodataminer save finish') 
        print('meteodataminer update finish')
        
    def startParse(self, startDate):
        citySet, data = self.mineData(startDate)
        print('Data parsing finished', len(citySet), len(data))
        return self.convertData(citySet, data)

    def mineData(self, start, url='https://meteopost.com/weather/archive/'):
        resultList = []
        monthSet = {'value': 0, 'text': 0}
        yearSet = {'value': 0, 'text': 0}
        citySet = {'value': 0, 'text': 0}
        badCitySet = {'value': 0, 'text': 0}
        # get city
        r = requests.get(url)
        html = bs(r.content, 'html.parser')
        badCitySet['value'], badCitySet['text'] = self._getSetData(name='city', html=html, part=0)
        citySet['value'], citySet['text'] = self._getSetData(name='city', html=html, part=1)
        # get month and year
        yearSet['value'], yearSet['text'] = self._getSetData(name='y', html=html, part=0)
        monthSet['value'], monthSet['text'] = self._getSetData(name='m', html=html, part=0)
        r.close()
        startParseFlag = False
        html = ''
        for year in yearSet['value']:
            for month in monthSet['value']:
                daysInMonthCount = str(monthrange(int(year), int(month))[1])
                try:
                    for city in citySet['value']:
                        if int(month) > start.month and int(year) >= start.year and city == citySet['value'][0]:
                            startParseFlag = True
                        if not startParseFlag:
                            continue
                        requestTemplate = 'd=1&m={}&y={}&city={}&arc=2&days={}'.format(month, year, city, daysInMonthCount)
                        headerData = {
                            "Host": "meteopost.com",
                            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Content-Length": "39",
                            "Origin": "https://meteopost.com",
                            "DNT": "1",
                            "Connection": "keep-alive",
                            "Referer": "https://meteopost.com/weather/archive/",
                            "Cookie": "_ga=GA1.2.1952077172.1608990993; _gid=GA1.2.2059205127.1609852737; _gat=1",
                            "Upgrade-Insecure-Requests": "1",
                            "TE": "Trailers"
                        }
                        time.sleep(0.1) # not to ddos timer)
                        r = requests.post(url, data=requestTemplate.encode(), headers=headerData, stream=True)
                        html = bs(r.content, 'html5lib')
                        items = html.find_all("table")
                        html = items[3]
                        items = html.find_all("tr")
                        for i in range(len(items)):
                            s = ''
                            tr = items[i]
                            if len(tr) > 5:
                                for child in tr:
                                    x = child.center
                                    try:
                                        img = x.img
                                        num = 0
                                        if img['src'] == '/pic/180.png':
                                            num = 0
                                        elif img['src'] == '/pic/225.png':
                                            num = 1
                                        elif img['src'] == '/pic/270.png':
                                            num = 2
                                        elif img['src'] == '/pic/360.png':
                                            num = 3
                                        elif img['src'] == '/pic/0.png':
                                            num = 4
                                        elif img['src'] == '/pic/45.png':
                                            num = 5
                                        elif img['src'] == '/pic/90.png':
                                            num = 6
                                        elif img['src'] == '/pic/135.png':
                                            num = 7
                                        elif img['src'] == '/pic/00.png':
                                            num = 8
                                        s = s + '_' + str(num)
                                    except:
                                        try:
                                            b = x.b
                                            s = s + '_' + b.string
                                        except: 
                                            #  set _ symbol for delimiter 
                                            if not isinstance(x, type(None)):
                                                s = s + '_' + x.get_text()
                                            else:
                                                s = s + '_=' # if data missing = symbol is placeholder
                            resultList.append(s + '&&' + requestTemplate + '\n')
                        r.close()
                except:
                    print(html)
                    return citySet, resultList
        return citySet, resultList

    def _getSetData(self, name='', html='', part=0):
        items = html.find_all(attrs={'name': name})
        temp1 = []
        temp2 = []
        for child in items[part].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        return temp1, temp2

    def convertData(self, citySet, data):
        resultList = []
        r = re.compile('^days=[0-9](2)[\n]$')
        i = 0
        while True:
            if i + 1 >= len(data):
                break
            line = data[i]
            nextLine = data[i+1]
            temp = str(line[-1:-9:-1])
            if temp[::-1] not in ('days=28\n', 'days=29\n', 'days=30\n', 'days=31\n'):
                data[i] = data[i].rstrip() + nextLine
                data.pop(i+1)
            i = i + 1
        i = 0
        headers = []
        while True:
            if i >= len(data):
                break
            line = data[i]
            baseList = line.split('&&')
            if line[0] == '&':
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
                    d.update({headers[j]: 0})
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
            resultList.append(d)
            i = i + 1
                #11-3
                #4-10
        for d in resultList:
            tempTime = str(d['Час']).split(':')[0]
            if tempTime == '24':
                tempTime = '0'
            tempDate = 0
            try:
                tempDate = datetime(year=int(d['y']), month=int(d['m']), day=int(d['День']), hour=int(tempTime))
            except:
                tempDate = datetime(year=int(d['y']), month=int(d['m']), day=1, hour=int(tempTime))
            d.update({
                'fullDate': tempDate,
                'cityName': citySet['text'][citySet['value'].index(d['city'])]
            })
        return citySet, resultList
        