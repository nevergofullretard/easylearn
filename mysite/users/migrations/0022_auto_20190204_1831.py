# Generated by Django 2.1.2 on 2019-02-04 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('units', '0008_unit_words_word_bei_preufung_falsch'),
        ('users', '0021_words_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='words_user',
            name='word',
        ),
        migrations.AddField(
            model_name='words_user',
            name='word',
            field=models.ManyToManyField(to='units.Unit_words'),
        ),
    ]
