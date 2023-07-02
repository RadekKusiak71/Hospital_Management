from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator,MaxLengthValidator

    
class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        if self.status:
            return f'Appointment Confirmed for {self.patient.firstname} {self.patient.lastname} - doctor {self.doctor.firstname} {self.doctor.lastname} in {self.room.number} - {self.date}'
        else:
            return f'Appointment Unconfirmed for {self.patient.firstname} {self.patient.lastname} - doctor {self.doctor.firstname} {self.doctor.lastname} in {self.room.number} - {self.date}'

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self) -> str:
        return f'{self.name} - {self.price}'
    
class Perscription(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField(null=True)
    status = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return f'{self.patient.firstname} - {self.patient.lastname} perscription number {self.id}'

class PerscriptionItems(models.Model):
    perscription = models.ForeignKey(Perscription,on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Perscription number: {self.perscription.id}'
    
class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    doctors = models.ManyToManyField(Doctor,related_name='participants')
    created_by = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room',on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return f'Meeting at {self.date} in {self.room.number} about {self.title}'
    
class Room(models.Model):
    number = models.IntegerField(validators=[
            MaxValueValidator(200),
            MinValueValidator(1)
        ])
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.number}'
    
class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciver')
    title = models.CharField(max_length=200,null=False,default='')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    readed_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'From {self.sender} to {self.reciver}'