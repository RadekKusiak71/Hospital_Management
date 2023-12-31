# Generated by Django 4.2.2 on 2023-07-01 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='perscription',
            name='number',
            field=models.CharField(default='0000', max_length=5, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.MaxLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(1)]),
        ),
    ]
