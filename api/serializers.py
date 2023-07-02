from rest_framework import serializers

from main.models import Patient,Doctor,Appointment,Medicine,Perscription,Message,PerscriptionItems


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('user',)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('user',)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"

class PerscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perscription
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        
class PerscriptionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerscriptionItems
        fields = "__all__"
