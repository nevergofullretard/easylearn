# Generated by Django 2.1.2 on 2019-01-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190115_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='voc_bits',
            field=models.IntegerField(default=10),
        ),
    ]
