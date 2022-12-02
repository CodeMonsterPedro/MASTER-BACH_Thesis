# Generated by Django 3.2.7 on 2022-11-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastMeteodata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(verbose_name='Date_and_time')),
                ('place', models.BigIntegerField(verbose_name='Place_id')),
                ('temperature', models.FloatField(verbose_name='Air temperature')),
                ('wind_way', models.BigIntegerField(verbose_name='Wind way')),
                ('wind_speed', models.FloatField(verbose_name='Wind speed')),
                ('air_pressure', models.FloatField(verbose_name='Pressure')),
                ('water_pressure', models.FloatField(verbose_name='Sea_level_pressure')),
                ('weather', models.TextField(verbose_name='Weather')),
            ],
            options={
                'verbose_name': 'Forecast',
                'verbose_name_plural': 'Forecast',
            },
        ),
        migrations.CreateModel(
            name='Meteodata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(verbose_name='Date_and_time')),
                ('place', models.BigIntegerField(verbose_name='Place_id')),
                ('place_name', models.CharField(max_length=80, verbose_name='Place_name')),
                ('temperature', models.FloatField(verbose_name='Air temperature')),
                ('wind_way', models.BigIntegerField(verbose_name='Wind way')),
                ('wind_speed', models.FloatField(verbose_name='Wind speed')),
                ('air_pressure', models.FloatField(verbose_name='Pressure')),
                ('water_pressure', models.FloatField(verbose_name='Sea_level_pressure')),
                ('weather', models.TextField(verbose_name='Weather')),
            ],
            options={
                'verbose_name': 'Meteodata',
                'verbose_name_plural': 'Meteodata',
            },
        ),
        migrations.CreateModel(
            name='MeteodataAnomalies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meteodata_pk', models.BigIntegerField(verbose_name='Record_id')),
                ('fieldname', models.TextField(verbose_name='Field_name')),
                ('value', models.TextField(verbose_name='Value')),
                ('anomaly', models.TextField(verbose_name='Anomaly')),
            ],
            options={
                'verbose_name': 'Anomalies',
                'verbose_name_plural': 'Anomalies',
            },
        ),
        migrations.CreateModel(
            name='NeuralNet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('file_data', models.FileField(upload_to='models/')),
                ('target', models.BigIntegerField(verbose_name='Target')),
                ('metric', models.BigIntegerField(verbose_name='Metric')),
                ('description', models.TextField(verbose_name='Description')),
                ('conclusion', models.TextField(verbose_name='Conclusion')),
            ],
            options={
                'verbose_name': 'NeuralNet',
                'verbose_name_plural': 'NeuralNet',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('neuralnet_id', models.BigIntegerField(verbose_name='NeuralNet_id')),
                ('test_date', models.DateTimeField(verbose_name='Date_and_time')),
                ('conclusion', models.TextField(verbose_name='Conclusion')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Test',
            },
        ),
    ]
