from django.urls import path
from . import views

urlpatterns = [
    path('',views.DashboardPage.as_view(),name='dashboard'),
    path('docreg/',views.DoctorRegisterPage.as_view(),name='doctor_register_page'),
    path('doclog/',views.DoctorLoginPage.as_view(),name='doctor_login_page'),
    path('doclogout/',views.DoctorLogout.as_view(),name='doctor_logout'),
    path('calendar/',views.CalendarPage.as_view(),name='doctor_calendar'),
    path('messages/',views.MessagesPage.as_view(),name='doctor_messages'),
    path('messages/<int:msg_id>',views.MessagePage.as_view(),name='doctor_message'),
]