# flake8: noqa
# Generated by Django 2.2.16 on 2020-10-12 20:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Update time'),
        ),
    ]