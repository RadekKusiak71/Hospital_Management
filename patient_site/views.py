from django.shortcuts import render,redirect
from django.views import View
from main.models import Patient,Apointment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import calendar
import datetime
from datetime import timedelta

class HomePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home_page_logged')
        context = {}
        return render(request,'patient_page/home.html',context)

method_decorator(login_required,name='dispatch')
class HomePageLogged(View):
    def get(self,request):
        patient = Patient.objects.get(user=request.user)
        apointments = Apointment.objects.filter(patient=patient).order_by('date')
        apointments_list = self.check_dates(apointments)
        context = {'apointment':apointments_list[0],'patient':patient}
        return render(request,'patient_page/home_log.html',context)
    
    def post(self,request):
        if 'delete' in request.POST:
            Apointment.objects.get(id=request.POST.get('delete')).delete()
        return redirect('home_page_logged')

    def check_dates(self, objects):
        today = timezone.now()
        obj_list = []
        for apointment in objects:
            if apointment.date > today:
                obj_list.append(apointment)
            else:
                apointment.delete()
        return obj_list
    

class AppointmentsPage(View):
    today = datetime.date.today()

    def get(self, request):
        day = datetime.date.today()
        calendar = self.get_calendar(AppointmentsPage.today)
        days = self.get_days(calendar)
        appointments = self.get_user_appointments()

        if 'next' in request.GET:
            AppointmentsPage.today += timedelta(days=31)
            calendar = self.get_month(AppointmentsPage.today)
            days = self.get_days(calendar)
            return redirect('appointments_page')
        
        elif 'last' in request.GET:
            if AppointmentsPage.today < datetime.date.today():
                calendar = self.get_month(AppointmentsPage.today)
                return redirect('appointments_page')
            else:
                AppointmentsPage.today -= timedelta(days=31)
                calendar = self.get_month(AppointmentsPage.today)
                days = self.get_days(calendar)
                return redirect('appointments_page')
            
        elif 'start_day' in request.GET:
                AppointmentsPage.today = datetime.date.today()
                calendar = self.get_month(AppointmentsPage.today)
                days = self.get_days(calendar)
                return redirect('appointments_page')
            
        context = {'calendar': calendar, 'days': days,'today_date':day,'appointments':appointments}
        return render(request, 'patient_page/appointments.html', context)

    def get_calendar(self,today):
        cal = calendar.Calendar()
        month_calendar = list(cal.monthdatescalendar(today.year,today.month))
        return month_calendar
    
    def get_days(self,month_calendar):
        days_list = []
        for week in month_calendar:
            for date in week:
                days_list.append(date)
        return days_list
    
    def get_month(self,today):
        cal = calendar.Calendar()
        month_calendar = list(cal.monthdatescalendar(today.year,today.month))
        return month_calendar
    
    def get_user_appointments(self):
        patient = Patient.objects.get(user=self.request.user)
        appointments = Apointment.objects.filter(patient=patient)
        return appointments


class PerscriptionPage(View):
    def get(self,request):
        context = {}
        return render(request,'patient_page/perscription.html',{})