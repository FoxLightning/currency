# Generated by Django 2.2.16 on 2020-10-06 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.PositiveSmallIntegerField(),
        ),
    ]