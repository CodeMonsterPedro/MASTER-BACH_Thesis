from .ForecastSummaryModel import ForecastSummaryModel
from .SimpleForecastModel import SimpleForecastModel


class ForecastDeamon:

    def __init__(self):
        self._summary = ForecastSummaryModel()
        self._simple = SimpleForecastModel()

    def update(self):
        self._makeSummary(self._updateShort())

    def _updateShort(self):
        return self._simple.update()

    def _makeSummary(self):
        return self._summary.getForecastSummary()
