# Generated by Django 2.1.2 on 2019-04-16 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0064_confirm_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirm_email',
            name='user',
        ),
        migrations.DeleteModel(
            name='Confirm_email',
        ),
    ]
