from django.db import models


class Test(models.Model):

    test_members = models.TextField("Members_list")
    test_date = models.DateTimeField("Date_and_time")
    test_records = models.TextField("Test_records_list")

    def __str__(self):
        return "({})members: {}".format(self.pk, self.test_records)

    class Meta:

        verbose_name = "Test"
        verbose_name_plural = "Test"


class Test_Record(models.Model):

    neuralnet_id = models.BigIntegerField("NeuralNet_id")
    summary_result = models.CharField("Summary result", max_length=80)
    forecast_result = models.CharField("Forecast result", max_length=80)
    anomalies_result = models.CharField("Anomalies result", max_length=80)

    def __str__(self):
        return "({})--{}".format(self.pk, self.neuralnet_id)

    class Meta:

        verbose_name = "Test_Record"
        verbose_name_plural = "Test_Record"


class NeuralNet(models.Model):

    name = models.CharField("Name", max_length=80)
    file_data = models.FileField(upload_to='models/')
    description = models.TextField("Description")

    def __str__(self):
        return "({})--{}".format(self.pk, self.name)

    class Meta:

        verbose_name = "NeuralNet"
        verbose_name_plural = "NeuralNet"


class Place(models.Model):

    name = models.CharField("Name", max_length=80)
    x = models.FloatField("geoX")
    y = models.FloatField("geoY")

    def __str__(self):
        return "({})--{}".format(self.pk, self.name)

    class Meta:

        verbose_name = "Region"
        verbose_name_plural = "Region"


class Meteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
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


class ClearMeteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
    temperature = models.FloatField("Air temperature")
    wind_way = models.BigIntegerField("Wind way")
    wind_speed = models.FloatField("Wind speed")
    air_pressure = models.FloatField("Pressure")
    water_pressure = models.FloatField("Sea_level_pressure")
    weather = models.TextField("Weather")

    def __str__(self):
        return self.pk

    class Meta:

        verbose_name = "Clean meteodata"
        verbose_name_plural = "Clean meteodata"


class ForecastMeteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
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


class ClearForecastMeteodata(models.Model):

    datetime = models.DateTimeField("Date_and_time")
    place = models.BigIntegerField("Place_id")
    temperature = models.FloatField("Air temperature")
    wind_way = models.BigIntegerField("Wind way")
    wind_speed = models.FloatField("Wind speed")
    air_pressure = models.FloatField("Pressure")
    water_pressure = models.FloatField("Sea_level_pressure")
    weather = models.TextField("Weather")

    def __str__(self):
        return self.pk

    class Meta:

        verbose_name = "Clean forecast"
        verbose_name_plural = "Clean forecast"


class MeteodataAnomalies(models.Model):

    meteodata_pk = models.BigIntegerField("Record_id")
    fieldname = models.TextField("Field_name")
    value = models.TextField("Value")
    anomaly = models.TextField("Anomaly")

    class Meta:
        verbose_name = "Anomalies"
        verbose_name_plural = "Anomalies"

    def __str__(self):
        return self.pk