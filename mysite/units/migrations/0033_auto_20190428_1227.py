# Generated by Django 2.1.2 on 2019-04-28 10:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0032_auto_20190419_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='anfrage_schule',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='anfrage_sprache',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='anfrage_unit',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
