# Generated by Django 2.1.2 on 2019-03-21 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0019_auto_20190321_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit_name',
            name='schule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unit_schule'),
        ),
        migrations.AlterField(
            model_name='unit_name',
            name='sprache',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unit_sprache'),
        ),
    ]
