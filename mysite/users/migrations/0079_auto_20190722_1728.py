# Generated by Django 2.1.2 on 2019-07-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0078_images_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
