# Generated by Django 2.1.2 on 2019-03-21 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0013_auto_20190321_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit_name',
            name='schule',
        ),
        migrations.DeleteModel(
            name='Unit_schule',
        ),
    ]
