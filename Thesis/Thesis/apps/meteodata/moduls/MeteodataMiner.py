from .Parser import MyParser
from .DB import DBControl
from datetime import datetime


class MeteodataMiner:

    def __init__(self):
        self._db = DBControl()
        self._parser = MyParser()

    def meteodataUpdateStatus(self):
        return False

    def updateMeteodata(self):
        print('meteodataminder update')
        lists = []
        citySet, listt = self._parser.StartParse()
        lists.append(listt)
        data = self._join(lists)
        print(data[:100])
        #self._save(citySet, data)

    def _join(self, lists=[]):
        print('meteodataminder join')
        resultList = []
        if len(lists) <= 1:
            return lists
        else:
            for l in lists:
                resultList += l
            return resultList

    def _save(self, citySet, data):
        print('meteodataminder save')
        for row in data:
            d = datetime(year=row['y'], month=row['m'], day=row['День'], hour=row['Час'])
            self._db.insertMeteodata([d, row['city'], citySet[row['city']], row['Темп. Возд'], row['Ветер'], row['Скор ветра'], row['Давл станц'], row['Давл моря'], row['Явления погоды']])
        self._db.save()

    