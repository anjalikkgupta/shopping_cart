# Generated by Django 3.0.3 on 2020-02-07 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200207_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='unit',
        ),
    ]
