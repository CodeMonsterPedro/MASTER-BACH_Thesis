from .Parser import MyParser
from .DB import DBControl
from datetime import datetime, timedelta


class MeteodataMiner:

    def __init__(self):
        self._db = DBControl()
        self._parser = MyParser()
        self._data = []
        self._citySet = []

    def meteodataUpdateStatus(self):
        return False

    def get(self):
        return (self._citySet, self._data)

    def getLastDate(self):
        tmp = self._db.getMeteodata(filter='DISTINCT datetime', where='ORDER BY datetime DESC')
        print(tmp)
        return tmp[0]

    def updateMeteodata(self):
        print('meteodataminder update')
        startDate = self.getLastDate()
        lists = []
        citySet, listt = self._parser.StartParse(start = startDate + timedelta(days=1))
        lists.append(listt)
        data = self._join(lists)
        print(data[:100])
        self._data = data
        self._citySet = citySet
        
    def _join(self, lists=[]):
        print('meteodataminder join')
        resultList = []
        if len(lists) <= 1:
            return lists
        else:
            for l in lists:
                for row in l:
                    resultList.append(row)
            resultList.sort(key=self.keyFunction)
        return resultList

    def keyFunction(self, row):
        d = datetime.today()
        tmp = datetime.strptime(row[1], '%Y-%m-%d %S:%M:%H')
        return d-tmp

    def save(self):
        print('meteodataminer save')
        for row in self._data:
            d = datetime(year=row['y'], month=row['m'], day=row['День'], hour=row['Час'])
            self._db.insertMeteodata([d, row['city'], self._citySet[row['city']], row['Темп. Возд'], row['Ветер'], row['Скор ветра'], row['Давл станц'], row['Давл моря'], row['Явления погоды']])
        self._db.save()
        self._data = []
        self._citySet = []

    