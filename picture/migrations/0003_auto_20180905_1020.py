# Generated by Django 2.0 on 2018-09-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_auto_20180904_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictureentry',
            name='negative',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pictureentry',
            name='positive',
            field=models.IntegerField(default=0),
        ),
    ]
