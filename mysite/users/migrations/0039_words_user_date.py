# Generated by Django 2.1.2 on 2019-02-10 09:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_words_user_fuer_pruefung'),
    ]

    operations = [
        migrations.AddField(
            model_name='words_user',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
