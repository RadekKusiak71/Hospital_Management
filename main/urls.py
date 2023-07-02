from django.urls import path
from . import views

urlpatterns = [
    path('',views.DashboardPage.as_view(),name='dashboard'),
    path('calendar/',views.CalendarPage.as_view(),name='doctor_calendar'),
    path('messages/',views.MessagesPage.as_view(),name='doctor_messages'),
    path('messages/<int:msg_id>',views.MessagePage.as_view(),name='doctor_message'),
    path('perscription/',views.PerscriptionCreate.as_view(),name='doctor_perscription'),
    path('perscription/<int:user_id>/',views.PerscriptionCreateForm.as_view(),name='perscription_create'),
    path('appointment/',views.CreateAppointment.as_view(),name='doctor_appointments'),
    path('appointment/<int:patient_id>',views.CreateAppointmentForm.as_view(),name='doctor_appointments_create'),
    path('patient/create/',views.CreatePatient.as_view(),name='doctor_patient_create'),
    
    path('docreg/',views.DoctorRegisterPage.as_view(),name='doctor_register_page'),
    path('doclog/',views.DoctorLoginPage.as_view(),name='doctor_login_page'),
    path('doclogout/',views.DoctorLogout.as_view(),name='doctor_logout'),
]