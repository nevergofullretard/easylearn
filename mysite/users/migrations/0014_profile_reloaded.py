# Generated by Django 2.1.2 on 2019-01-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_profile_user_zurueck'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reloaded',
            field=models.IntegerField(default=0),
        ),
    ]
