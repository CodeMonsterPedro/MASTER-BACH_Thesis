from .Parser import MyParser
from .DB import DBControl
from datetime import datetime, timedelta


class MeteodataMiner:

    def __init__(self):
        self._db = DBControl()
        self._parser = MyParser()
        self._data = []
        self._citySet = []
        self._rowsCount = 0

    def meteodataUpdateStatus(self):
        return False

    def get(self):
        return (self._citySet, self._data, self._rowsCount)

    def getLastDate(self):
        tmp = self._db.getMeteodata(filter='DISTINCT datetime', where='ORDER BY datetime DESC')
        print(tmp)
        return tmp[0]

    def updateMeteodata(self):
        print('meteodataminder update')
        startDate = self.getLastDate()
        lists = []
        citySet, listt, rowsCount = self._parser.StartParse(start = startDate + timedelta(days=1))
        lists.append(listt)
        data = []
        if rowsCount > 1:
            data = self._join(lists, 2)
        else:
            data = self._join(lists, 1)
        print(data)
        self._data = data
        self._citySet = citySet
        self._rowsCount = rowsCount
        
    def _join(self, lists=[], ttype=2):
        print('meteodataminder join')
        resultList = []
        if ttype == 1:
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

    