# Generated by Django 3.0.3 on 2020-02-07 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('disc_price', models.FloatField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Quantity')),
            ],
        ),
    ]
