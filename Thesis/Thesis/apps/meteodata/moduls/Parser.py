import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from calendar import monthrange
import psycopg2
import time
import re
from datetime import date


class MyParser:

    def __init__(self):
        self._rawData = []
        self._urls = ['https://meteopost.com/weather/archive/']
        self._conn = psycopg2.connect(dbname='Weather', user='postgres', password='12345', host='localhost')
        self._curs = self._conn.cursor()
        self._f = 0

    def StartParse(self):
        citySet = self.raw_update1()
        self.prepare_data1(citySet)
        if not isinstance(p._f, int):
            p._f.close()
        p._curs.close()
        p._conn.close()

    def raw_update1(self, url='https://meteopost.com/weather/archive/', begin='', end=''):
        try:
            self._f.close()
        except:
            self._f = 0
        self._f = open('/home/max/Projects/BACH_Thesis/data.txt', 'a+')
        monthSet = {'value': 0, 'text': 0}
        yearSet = {'value': 0, 'text': 0}
        citySet = {'value': 0, 'text': 0}
        badCitySet = {'value': 0, 'text': 0}
        # get city
        r = requests.get(url)
        html = bs(r.content, 'html.parser')
        items = html.find_all(attrs={'name': 'city'})
        temp1 = []
        temp2 = []
        for child in items[0].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        badCitySet['value'] = temp1
        badCitySet['text'] = temp2
        temp1 = []
        temp2 = []
        for child in items[1].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        citySet['value'] = temp1
        citySet['text'] = temp2
        # get month and year
        temp1 = []
        temp2 = []
        items = html.find_all(attrs={'name': 'y'})
        for child in items[0].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        yearSet['value'] = temp1
        yearSet['text'] = temp2
        temp1 = []
        temp2 = []
        items = html.find_all(attrs={'name': 'm'})
        for child in items[0].children:
            if not isinstance(child, NavigableString):
                temp1.append(child['value'])
                temp2.append(child.string)
        monthSet['value'] = temp1
        monthSet['text'] = temp2
        r.close()
        flag = False
        for year in yearSet['value']:
            d = '1'
            y = year
            arc = '2'
            for month in monthSet['value']:
                m = month
                days = str(monthrange(int(y), int(m))[1])
                for city in citySet['value']:
                    city = city
                    req = 'd={}&m={}&y={}&city={}&arc=2&days={}'.format(d, m, y, city, days)
                    print(req)
                    hd = {
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
                    if req == begin or begin == '':
                        flag = True
                    if not flag:
                        continue
                    if req == end:
                        return
                    time.sleep(0.15)
                    r = requests.post(url, data=req.encode(), headers=hd, stream=True)
                    html = bs(r.content, 'html5lib')
                    items = html.find_all("table")
                    print(len(items))
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
                                        if not isinstance(x, type(None)):
                                            s = s + '_' + x.get_text()
                                        else:
                                            s = s + '_='
                        print('SSS - ', s)
                        self._f.write(s)
                        self._f.write('&&' + req)
                        self._f.write('\n')
                    r.close()
        self._f.close()
        return citySet

    def prepare_data1(self, citySet):
        self._f = open('/home/max/Projects/BACH_Thesis/data', 'r')
        lines = self._f.readlines()
        r = re.compile('^days=[0-9](2)[\n]$')
        i = 0
        while True:
            line = lines[i]
            nextLine = lines[i+1]
            temp = str(line[-1:-9:-1])
            if temp[::-1] not in ('days=28\n', 'days=29\n', 'days=30\n', 'days=31\n'):
                print(list(temp[::-1]))
                lines[i] = lines[i].rstrip() + nextLine
                lines.pop(i+1)
            i = i + 1
            if i + 1 == len(lines):
                break
        self._f.close()
        self._f = open('/home/max/Projects/BACH_Thesis/data', 'w')
        self._f.writelines(lines)
        i = 0
        headers = []
        while True:
            line = lines[i]
            baseList = line.split('&&')
            if line[0] == '&':
                print(baseList[1])
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
            self._curs.execute("INSERT INTO public.meteodata VALUES(DEFAULT, '" + str(d['y']) + "-" + str(d['m']) + "-" + str(d['День']) + " " + str(d['Час']) + ":00', " + str(d['city']) + ", '" + citySet[d['city']] + "', " + str(d['Темп. Возд']) + ", " + str(d['Ветер']) + ", " + str(d['Скор ветра']) + ", " + str(d['Давл станц']) + ", " + str(d['Давл моря']) + ", '{" + str(d['Явления погоды']) + "}')")
            self._conn.commit()
            i = i + 1        
                #11-3
                #4-10 
            if i == len(lines):
                break
        self._f.close()     

if __name__ == "__main__":
    pass