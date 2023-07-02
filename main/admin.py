from django.contrib import admin
from main.models import Patient,Doctor,Apointment,Medicine,Perscription,Meeting,Room,Message,PerscriptionItems

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Apointment)
admin.site.register(Medicine)
admin.site.register(Perscription)
admin.site.register(Meeting)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PerscriptionItems)