# Generated by Django 4.1.7 on 2023-03-27 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floormodel',
            name='floorNumber',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]
