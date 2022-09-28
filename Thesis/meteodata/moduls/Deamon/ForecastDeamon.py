from .ForecastSummaryModel import ForecastSummaryModel
from .SimpleForecastModel import SimpleForecastModel
from .AnomalyModel import AnomalyModel
from ..MeteodataMiner import MeteodataMiner
from datetime import datetime
import matplotlib.pyplot as plt
from ..DB import DBControl


class ForecastDeamon:

    def __init__(self):
        #self._summary = ForecastSummaryModel('fullconnect', 'meteodata_forecastmeteodata')
        #self._summaryClear = ForecastSummaryModel('fullconnect_clear', 'meteodata_clearforecastmeteodata')
        #self._simple = SimpleForecastModel('rnn', 'meteodata_meteodata')
        #self._simpleClear = SimpleForecastModel('rnn_clear', 'meteodata_clearmeteodata')
        #self._anomaly = AnomalyModel()
        self._miner = MeteodataMiner()
        self._db = DBControl()
        self._cacheFile = 0
        self._lastRecordsCount = 0
        self._lastClearRecordsCount = 0
        self._lastAnomaliesCount = 0
        self._lastRecordsAccuracy = 0
        self._lastClearRecordsAccuracy = 0
        self._img_path = '../../static/saved_figure.png'

    def _prepareMeteodataForTest(self):
        self._miner.updateMeteodata()
        citySet, lists, count = self._miner.get()
        clearList = self._anomaly.filter(lists, count)
        self._anomaly.save()
        for row in lists:
            self._db.insertMeteodata(row)
        for row in clearList:
            self._db.insertClearMeteodata(row)
        return (lists, clearList, count)

    def _prepareModelsForTest(self, rowList, clearList, count):
        predictions = self._simple.predict(rowList, count)
        predictionsClear = self._simpleClear.predict(clearList, count)
        predictions_summery = self._summary.predict(predictions, count)
        predictionsClear_summery = self._summaryClear.predict(predictionsClear, count)
        resultPrediction = []
        resultPredictionClear = []
        for i in range(len(predictions)):
            predictions[i].append(predictions_summery[i])
            resultPrediction.append(predictions[i])
        for i in range(len(predictionsClear)):
            predictionsClear[i].append(predictionsClear_summery[i])
            resultPredictionClear.append(predictionsClear[i])
        for row in resultPrediction:
            self._db.insertForecast(row)
        for row in resultPredictionClear:
            self._db.insertClearForecast(row)

        return (resultPrediction, resultPredictionClear)

    def _updateShort(self):
        self._simple.update()

    def _makeSummary(self):
        self._summary.getForecastSummary()

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

    def makeTest(self):
        print('good test')
        rowList, clearList, count = self._prepareMeteodataForTest()
        self._lastRecordsCount = len(rowList)
        self._lastClearRecordsCount = len(clearList)
        self._lastAnomaliesCount = self._anomaly.getStatistic()
        resultList, resultListClear = self._prepareModelsForTest(rowList, clearList, count)
        self._lastRecordsAccuracy = self._simple.getStatistic()
        self._lastClearRecordsAccuracy = self._simpleClear.getStatistic()
        clearDataPercent = len(resultListClear) / (len(resultList)/100)
        sizes = [clearDataPercent, abs(clearDataPercent - 100)]
        fig1, ax1 = plt.subplots(1, 2)
        ax1[0].bar(['All', 'Anomalies'], [len(resultList), len(resultList) - len(resultListClear)])
        ax1[1].pie(sizes, labels=['All', 'Anomalies'], autopct='%1.1f%%', shadow=True, startangle=90)
        ax1[1].axis('equal')
        plt.savefig('Thesis/Thesis/apps/meteodata/static/saved_figure.png')

    def update(self):
        self._updateShort()
        self._makeSummary()
        self._makeLog('forecast')

    def scanForAnomalies(self):
        self._anomaly.scan()
        self._makeLog('anomalies')

    def getLastRecordsCount(self):
        return self._lastRecordsCount
    
    def getLastClearRecordsCount(self):
        return self._lastClearRecordsCount

    def getLastAnomaliesCount(self):
        return self._lastAnomaliesCount

    def getLastResultAccuracy(self):
        return self._lastRecordsAccuracy

    def getLastClearResultAccuracy(self):
        return self._lastClearRecordsAccuracy

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

    
