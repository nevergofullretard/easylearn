# Generated by Django 2.1.2 on 2019-05-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_linked'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='viewed',
            field=models.TextField(default=''),
        ),
    ]
