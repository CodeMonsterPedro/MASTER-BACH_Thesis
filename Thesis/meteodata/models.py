from django.db import models


class Test(models.Model):

    neuralnet_id = models.BigIntegerField("NeuralNet_id")
    datetime = models.DateTimeField("Date_and_time")
    conclusion = models.TextField("Conclusion")# accurancy:... 

    def __str__(self):
        return "({})members: {}".format(self.pk, self.test_records)

    class Meta:

        verbose_name = "Test"
        verbose_name_plural = "Test"


class NeuralNet(models.Model):

    name = models.CharField("Name", max_length=80)
    file_data = models.FileField('NetFile', upload_to='models/')
    target = models.BigIntegerField("Target")# forecast - 1, summary - 2
    metric = models.BigIntegerField("Metric")
    description = models.TextField("Description")# layers count, neirons in layer, type of layers etc.
    conclusion = models.TextField("Conclusion")# importance of input parameters 

    def __str__(self):
        return "({})--{}".format(self.pk, self.name)

    def delete(self, *args, **kwargs):
        self.file_data.delete()
        super().delete(*args, **kwargs)

    class Meta:

        verbose_name = "NeuralNet"
        verbose_name_plural = "NeuralNet"


class Meteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
    place_name = models.CharField("Place_name", max_length=80)
    temperature = models.FloatField("Air temperature")
    wind_way = models.BigIntegerField("Wind way")
    wind_speed = models.FloatField("Wind speed")
    air_pressure = models.FloatField("Pressure")
    water_pressure = models.FloatField("Sea_level_pressure")
    weather = models.TextField("Weather")

    def __str__(self):
        return self.pk

    class Meta:

        verbose_name = "Meteodata"
        verbose_name_plural = "Meteodata"


class ForecastMeteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
    place_name = models.CharField("Place_name", max_length=80)
    temperature = models.FloatField("Air temperature")
    wind_way = models.BigIntegerField("Wind way")
    wind_speed = models.FloatField("Wind speed")
    air_pressure = models.FloatField("Pressure")
    water_pressure = models.FloatField("Sea_level_pressure")
    weather = models.TextField("Weather")

    def __str__(self):
        return self.pk

    class Meta:

        verbose_name = "Forecast"
        verbose_name_plural = "Forecast"
