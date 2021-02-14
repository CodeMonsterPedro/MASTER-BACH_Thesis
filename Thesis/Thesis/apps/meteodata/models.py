from django.db import models


class Meteodata(models.Model):

    id = models.BigAutoField("id", primary_key=True)
    datetime = models.DateTimeField("Дата и время")
    place = models.BigIntegerField("Код места")
    placeName = models.CharField("Место", max_length=80)
    temperature = models.FloatField("Температура воздуха")
    wind_way = models.BigIntegerField("Направление ветра")
    wind_speed = models.FloatField("Скорость ветра")
    air_pressure = models.FloatField("Атмосферное давление")
    water_pressure = models.FloatField("Давление моря")
    weather = models.TextField("Погодное явление")

    def __str__(self):
        return self.id

    class Meta:

        verbose_name = "Метеоданные"
        verbose_name_plural = "Метеоданные"


class ForecastMeteodata(models.Model):

    id = models.BigAutoField("id", primary_key=True)
    datetime = models.DateTimeField("Дата и время")
    place = models.BigIntegerField("Код места")
    placeName = models.CharField("Место", max_length=80)
    temperature = models.FloatField("Температура воздуха")
    wind_way = models.BigIntegerField("Направление ветра")
    wind_speed = models.FloatField("Скорость ветра")
    air_pressure = models.FloatField("Атмосферное давление")
    water_pressure = models.FloatField("Давление моря")
    weather = models.TextField("Погодное явление")

    def __str__(self):
        return self.id

    class Meta:

        verbose_name = "Спрогнозированные метеоданные"
        verbose_name_plural = "Спрогнозированные метеоданные"


class MeteodataAnomalies(models.Model):

    id = models.BigAutoField("id", primary_key=True)
    meteodata_id = models.BigIntegerField("Код записи")
    fieldname = models.TextField("Название поля")
    value = models.TextField("Значение")
    anomaly = models.TextField("Аномалия")

    class Meta:
        verbose_name = "Аномалии"
        verbose_name_plural = "Аномалии"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})