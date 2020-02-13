# Generated by Django 3.0.3 on 2020-02-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_quantity_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
