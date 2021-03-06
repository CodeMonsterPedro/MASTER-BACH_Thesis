from .ForecastSummaryModel import ForecastSummaryModel
from .SimpleForecastModel import SimpleForecastModel


class ForecastDeamon:

    def __init__(self):
        self._summary = ForecastSummaryModel()
        self._simple = SimpleForecastModel()
        self._anomaly = AnomalyModel()

    def update(self):
        self._updateShort()
        self._makeSummary()

    def scanForAnomalies(self):
        self._anomaly.scan()

    def _updateShort(self):
        self._simple.update()

    def _makeSummary(self):
        self._summary.getForecastSummary()
