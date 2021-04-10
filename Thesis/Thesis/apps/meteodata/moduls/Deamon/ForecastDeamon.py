from .ForecastSummaryModel import ForecastSummaryModel
from .SimpleForecastModel import SimpleForecastModel
from .AnomalyModel import AnomalyModel
from datetime import datetime


class ForecastDeamon:

    def __init__(self):
        self._summary = ForecastSummaryModel()
        self._simple = SimpleForecastModel()
        self._anomaly = AnomalyModel()
        self._cacheFile = 0

    def update(self):
        self._updateShort()
        self._makeSummary()
        self._makeLog('forecast')

    def scanForAnomalies(self):
        self._anomaly.scan()
        self._makeLog('anomalies')

    def forecastUpdateStatus(self):
        # ready in False
        try:
            self._cacheFile = open('cacheFile.txt', 'r')
            l = self._cacheFile.readlines()
            d = 0
            for i in range(len(l)):
                tmpL = l[i].split(': ')
                if tmpL[0] == 'forecast':
                    d = datetime.strptime(tmpL[1], "%Y-%m-%d %H:%M:%S")
            self._cacheFile.close()
            if (d - datetime.now()) > timedelta(hours=3):
                return False
            else:
                return True
        except:
            if not isinstance(self._cacheFile, int):
                self._cacheFile.close()
            return False

    def anomaliesScanStatus(self):
        try:
            self._cacheFile = open('cacheFile.txt', 'r')
            l = self._cacheFile.readlines()
            d = 0
            for i in range(len(l)):
                tmpL = l[i].split(': ')
                if tmpL[0] == 'anomalies':
                    d = datetime.strptime(tmpL[1], "%Y-%m-%d %H:%M:%S")
            self._cacheFile.close()
            if (d - datetime.now()) > timedelta(hours=3):
                return False
            else:
                return True
        except:
            if not isinstance(self._cacheFile, int):
                self._cacheFile.close()
            return False

    def _updateShort(self):
        self._simple.update()

    def _makeSummary(self):
        self._summary.getForecastSummary()

    def _make_test(self):
        print('good test')
        pass

    def _makeLog(self, name=''):        
        self._cacheFile = open('cacheFile.txt', 'r')
        l = self._cacheFile.readlines()
        newL = []
        for i in range(len(l)):
            tmpL = l[i].split(':')
            if tmpL[0] == name:
                continue
            newL.append(l[i])
        self._cacheFile.close()
        self._cacheFile = open('cacheFile.txt', 'w')
        newL.append(name + ": " + str(datetime.now()))
        self._cacheFile.writelines(newL)
        self._cacheFile.close()
