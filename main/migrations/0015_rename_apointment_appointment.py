# Generated by Django 4.2.2 on 2023-07-02 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_doctor_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Apointment',
            new_name='Appointment',
        ),
    ]
