# Generated by Django 3.2.7 on 2022-11-17 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meteodata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neuralnet',
            name='file_data',
            field=models.FileField(upload_to='models/', verbose_name='NetFile'),
        ),
    ]
