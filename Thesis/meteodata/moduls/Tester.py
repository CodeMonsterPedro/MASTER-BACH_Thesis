from ..models import NeuralNet, Test
from datetime import datetime
from .Deamon.ForecastSummaryModel import ForecastSummaryModel
from .Deamon.SimpleForecastModel import SimpleForecastModel
from ..forms import TestForm
import statistics


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
        conclusion = self.parametersImportantTest(examinerLoader)
        testResult = examinerLoader.test()
        print(testResult)
        self.saveConclusion(examiner_id, conclusion)
        self.saveTest(examiner_id, testResult)

    def parametersImportantTest(self, examinerLoader):
        conclusion = ''
        data = examinerLoader._neuralNetObject.layers[0].get_weights()[0]
        result = {}
        labels = examinerLoader.getHyperparametersLabels()
        for i in range(len(data)):
            result.update({labels[i]: abs(statistics.mean(data[i]))})
        important = labels[0]
        not_important = labels[0]
        for key, value in result.items():
            if value > result[important]:
                important = key
            if value < result[not_important]:
                not_important = key
        conclusion = 'Important: {} & Not important: {}'.format(important, not_important)
        print(result)
        return conclusion

    def saveConclusion(self, examiner_id, conclusion):
        obj = NeuralNet.objects.get(pk=examiner_id)
        obj.conclusion = conclusion
        obj.save()

    def saveTest(self, examiner_id, testResult):
        obj = Test.objects.all().filter(neuralnet_id=examiner_id)
        if len(obj) != 0:
            obj = Test.objects.get(neuralnet_id=examiner_id)
            obj.datetime=datetime.today()
            obj.conclusion=testResult
            obj.save()
        else:
            data = {
                'neuralnet_id': examiner_id,
                'datetime': datetime.today(), 
                'conclusion': testResult
            }
            form = TestForm(data)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

