from ..models import NeuralNet, Test
from datetime import datetime
from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel


class Tester:

    def __init__(self):
        pass

    def makeFullTest(self, examiner_id):
        obj = NeuralNet.objects.get(pk=examiner_id)
        examinerLoader = 0
        if obj.target == 1:
            examinerLoader = SimpleForecastModel(model_id=examiner_id)
        elif obj.target == 2:
            examinerLoader = ForecastSummaryModel(model_id=examiner_id)
        #conclusion = self.parametersImportantTest(examinerLoader)
        testResult = examinerLoader.test()
        print(testResult)
        #self.saveConclusion(examiner_id, conclusion)
        #self.saveTest(examiner_id, testResult)

    def parametersImportantTest(self, examinerLoader):
        conclusion = '-'
        # print(model.layers[0].get_weights()[0])
        # magic TODO add calculation of parameters importance
        return conclusion

    def saveConclusion(self, examiner_id, conclusion):
        obj = NeuralNet.objects.get(pk=examiner_id)
        obj.conclusion = conclusion
        obj.save()

    def saveTest(self, examiner_id, testResult):
        obj = Test(neuralnet_id=examiner_id, test_date=datetime.today(), conclusion=testResult)
        obj.save()