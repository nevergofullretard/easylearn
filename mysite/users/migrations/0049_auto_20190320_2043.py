# Generated by Django 2.1.2 on 2019-03-20 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_auto_20190320_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unit_name'),
        ),
    ]
