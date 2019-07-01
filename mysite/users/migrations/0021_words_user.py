# Generated by Django 2.1.2 on 2019-02-04 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0007_remove_unit_words_word_bei_preufung_falsch'),
        ('users', '0020_auto_20190202_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Words_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit_words')),
            ],
        ),
    ]
