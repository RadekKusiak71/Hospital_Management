from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from main.models import Patient,Doctor,Appointment,Medicine,Perscription,Room,Message,PerscriptionItems
from .serializers import PatientSerializer,DoctorSerializer,AppointmentSerializer,MedicineSerializer,PerscriptionSerializer,MessageSerializer,PerscriptionItemsSerializer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Patient':'/patient/',
        'Doctor':'/doctor/',
        'Appointment':'/patient/',
        'Medicine':'/patient/',
        'Perscription':'/patient/',
        'PerscriptionItems':'/patient/',
        'Room':'/patient/',
        'Message':'/patient/',
    }

    return Response(api_urls)

@api_view(['GET'])
def getPatients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDoctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAppointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMedicines(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPerscription(request):
    perscriptions = Perscription.objects.all()
    serializer = PerscriptionSerializer(perscriptions,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPerscriptionItems(request):
    perscription_items = PerscriptionItems.objects.all()
    serializer = PerscriptionItemsSerializer(perscription_items,many=True)
    return Response(serializer.data)
