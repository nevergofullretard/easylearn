# Generated by Django 2.1.2 on 2019-03-21 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0015_unit_schule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit_name',
            name='sprache',
        ),
    ]
