from django.utils import timezone
import calendar
import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

from main.models import Patient,Apointment,Perscription
from .forms import RegisterForm,UserLoginForm

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
        if apointments is None:
            apointments_list = self.check_dates(apointments)
            context = {'apointment':apointments_list[0],'patient':patient}
        else:
            apointments_list = []
            context = {'apointment':apointments_list,'patient':patient}
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
    
method_decorator(login_required,name='dispatch')
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

method_decorator(login_required,name='dispatch')
class PerscriptionPage(View):
    def get(self,request):
        persciptions = self.get_perscription()
        context = {'prescriptions':persciptions}
        return render(request,'patient_page/perscription.html',context)
    
    def get_perscription(self):
        return Perscription.objects.filter(patient=Patient.objects.get(user=self.request.user))
    

class LoginPage(View):
    def get(self,request):
        form = UserLoginForm()
        context = {'login_form':form}
        return render(request,'patient_page/login_page.html',context)
    
    def post(self,request):
        form = UserLoginForm(request,data=request.POST)
        return  self.form_validation(form,'home_page_logged')
    
    def form_validation(self,form,succes_url):
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(self.request,user)
                return redirect(succes_url)
            else:
                return HttpResponse('Invalid data try again later')
        else:
            return HttpResponse('Invalid data try again later')

class RegisterPage(View):
    def get(self, request):
        form = RegisterForm()
        context = {'register_form': form}
        return render(request, 'patient_page/register_page.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        return self.form_validation(form, 'login_page')

    def form_validation(self, form, success_url):
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                firstname=user.first_name,
                lastname=user.last_name,
                email=user.email,
                phone_number='000000000'
            )
            return redirect(success_url)
        else:
            return HttpResponse('Invalid data. Please try again later.')
        
method_decorator(login_required,name='dispatch')
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home_page')
    