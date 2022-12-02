from ..models import NeuralNet, Test
from datetime import datetime
from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel


class Tester:

    def __init__(self):
        self.metrics = [
            'AUC',
            'Accuracy',
            'BinaryCrossentropy',
            'CosineSimilarity',
            'FalseNegatives',
            'Hinge',
            'IoU',
            'KLDivergence',
            'Mean',
            'MeanAbsoluteError'
        ]

    def makeFullTest(self, examiner_id):
        obj = NeuralNet.objects.get(pk=examiner_id)
        examinerLoader = 0
        if obj.target == 1:
            examinerLoader = SimpleForecastModel(model_id=examiner_id)
        elif obj.target == 2:
            examinerLoader = ForecastSummaryModel(model_id=examiner_id)
        conclusion = self.parametersImportantTest(examinerLoader)
        testResult = self.test(examinerLoader)
        self.saveConclusion(examiner_id, conclusion)
        self.saveTest(examiner_id, testResult)

    def parametersImportantTest(self, examinerLoader):
        conclusion = '-'
        # magic TODO add calculation of parameters importance
        return conclusion

    def test(self, examinerLoader):
        testResult = ''
        for metric in self.metrics:
            testResult = testResult + ' {}: {};'.format(metric, examinerLoader.test(metric))
        return testResult

    def saveConclusion(self, examiner_id, conclusion):
        obj = NeuralNet.objects.get(pk=examiner_id)
        obj.conclusion = conclusion
        obj.save()

    def saveTest(self, examiner_id, testResult):
        obj = Test(neuralnet_id=examiner_id, test_date=datetime.today(), conclusion=testResult)
        obj.save()