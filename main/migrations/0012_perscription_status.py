# Generated by Django 4.2.2 on 2023-07-02 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_perscription_expire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='perscription',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]