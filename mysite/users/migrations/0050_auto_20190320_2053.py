# Generated by Django 2.1.2 on 2019-03-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_auto_20190320_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_unit',
            field=models.IntegerField(default=0),
        ),
    ]
