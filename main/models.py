from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=9)
    email = models.EmailField()

class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=9)
    email = models.EmailField()

class Apointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,null=True)

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Perscription(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    medicine = models.ManyToManyField(Medicine)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField()

class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    doctors = models.ManyToManyField(Doctor,related_name='participants')
    created_by = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,null=True)

class Room(models.Model):
    number = models.IntegerField(validators=[
            MaxValueValidator(200),
            MinValueValidator(1)
        ])
    status = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciver')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    readed_time = models.DateTimeField(null=True)
