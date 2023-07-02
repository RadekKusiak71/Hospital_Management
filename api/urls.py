from django.urls import path
from . import views

urlpatterns = [
    path('',views.apiOverview,name='api-overview'),
    path('patients/',views.getPatients,name='api-patients'),
    path('doctors/',views.getDoctors,name='api-doctors'),
    path('appointments/',views.getAppointments,name='api-appointments'),
    path('medicines/',views.getMedicines,name='api-medicines'),
    path('perscriptions/',views.getPerscription,name='api-perscriptions'),
    path('messages/',views.getMessages,name='api-messages'),
    path('perscription_items/',views.getPerscriptionItems,name='api-perscription_items'),

]