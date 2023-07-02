import calendar
import datetime
from datetime import timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from main.models import Patient,Doctor,Appointment,Medicine,Perscription,Meeting,Room,Message,PerscriptionItems
from .forms import MessageForm,DoctorRegisterForm,DoctorUserLoginForm

method_decorator(staff_member_required,name='dispatch')
class DashboardPage(View):
    def get(self,request):
        if request.user.is_staff:
            doctor = Doctor.objects.get(user=request.user)
            form = MessageForm()

            appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
            appointments_list = self.check_dates(appointments)

            meetings = Meeting.objects.filter(doctors=doctor).order_by('date')
            meetings_list = self.check_dates(meetings)
            context = {'appointments':appointments_list,
                    'message_form':form,
                    'meetings':meetings_list,
                    }
            return render(request,'main/dashboard.html',context)
        else:
            return HttpResponse('Only for staff members')
    
    def post(self,request):
        if 'msg_form' in request.POST:
            send_form = MessageForm(request.POST)
            return self.post_send_msg(send_form,request.user)
        elif 'delete' in request.POST:
            return self.post_delete_appointment()
        elif 'confirm' in request.POST:
            return self.post_confirm_appointment()
        
    def post_send_msg(self,send_form,sender):
        send_form.save(commit=False)
        send_form.instance.sender = sender
        send_form.save()
        return redirect('dashboard')

    def post_delete_appointment(self):
        appointment_id = self.request.POST.get('delete')
        Appointment.objects.get(id=appointment_id).delete()
        return redirect('dashboard')
    
    def post_confirm_appointment(self):
        appointment_id = self.request.POST.get('confirm')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = True
        appointment.save()
        return redirect('dashboard')
    
    def check_dates(self, objects):
        today = timezone.now()
        obj_list = []
        for apointment in objects:
            if apointment.date > today:
                obj_list.append(apointment)
        return obj_list
    
method_decorator(staff_member_required,name='dispatch')
class CalendarPage(View):
    today = datetime.date.today()

    def get(self, request):
        if request.user.is_staff:
            day = datetime.date.today()
            calendar = self.get_calendar(CalendarPage.today)
            days = self.get_days(calendar)
            appointments = self.get_user_appointments()
            days_list = self.update_list(appointments,days)

            if 'next' in request.GET:
                CalendarPage.today += timedelta(days=31)
                calendar = self.get_month(CalendarPage.today)
                days = self.get_days(calendar)
                days_list = self.update_list(appointments,days)
                return redirect('doctor_calendar')
            
            elif 'last' in request.GET:
                if CalendarPage.today < datetime.date.today():
                    calendar = self.get_month(CalendarPage.today)
                    return redirect('doctor_calendar')
                else:
                    CalendarPage.today -= timedelta(days=31)
                    calendar = self.get_month(CalendarPage.today)
                    days = self.get_days(calendar)
                    days_list = self.update_list(appointments,days)
                    return redirect('doctor_calendar')
                
            elif 'start_day' in request.GET:
                    CalendarPage.today = datetime.date.today()
                    calendar = self.get_month(CalendarPage.today)
                    days = self.get_days(calendar)
                    days_list = self.update_list(appointments,days)
                    return redirect('doctor_calendar')
            
            elif 'search_query' in request.GET:
                CalendarPage.today = datetime.date.today()
                calendar = self.get_month(CalendarPage.today)
                days = self.get_days(calendar)
                patients = self.search_query()
                appointments = self.search_appointments(patients)
                days_list = [[appointment] for appointment in appointments]
            
            context = {'calendar': calendar, 'days': days_list,'today_date':day,'appointments':appointments}
            return render(request, 'main/doctor_calendar.html', context)
        else:
            return HttpResponse('Only for staff members')
        
    def update_list(self, appointments, day_list):
        days_l = [[day] for day in day_list]
        for appointment in appointments:
            for day in days_l:
                if day[0].strftime("%Y-%m-%d") == appointment.date.strftime("%Y-%m-%d"):
                    day.append(appointment)
        return days_l
    
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
    
    def get_user_appointments(self):
        doctor = Doctor.objects.get(user=self.request.user)
        appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
        return appointments
    
    def get_month(self,today):
        cal = calendar.Calendar()
        month_calendar = list(cal.monthdatescalendar(today.year,today.month))
        return month_calendar

    def search_query(self):
        patient = self.request.GET.get('search_query')
        patient_list = []
        
        if Patient.objects.filter(firstname__contains = patient) is not None:
            for patient_data in Patient.objects.filter(firstname__contains = patient):
                patient_list.append(patient_data)
        elif Patient.objects.filter(lastname__contains = patient) is not None:
            print(Patient.objects.filter(lastname__contains = patient))
            for patient_data in Patient.objects.filter(lastname__contains = patient):
                patient_list.append(patient_data)
        return patient_list

    def search_appointments(self,patients):
        appointment_list = []
        for person in patients:
            appointments = Appointment.objects.filter(patient = person).order_by('date')
            for appointment in appointments:
                appointment_list.append(appointment)
        return appointment_list
    
method_decorator(staff_member_required,name='dispatch')
class MessagesPage(View):
    def get(self,request):
        if request.user.is_staff:
            msg_recived = Message.objects.filter(reciver = request.user)
            msg_sended = Message.objects.filter(sender = request.user)
            context = {'recived':msg_recived,'sended':msg_sended}
            return render(request,'main/messages.html',context)
        else:
            return HttpResponse('Only for staff memebers')
        
method_decorator(staff_member_required,name='dispatch')
class MessagePage(View):
    def get(self,request,msg_id):
        if request.user.is_staff:
            message = Message.objects.get(id=msg_id)
            message.readed = True
            message.save()
            context = {'message':message}
            return render(request,'main/message.html',context)
        else:
            return HttpResponse('Only for staff members')
    def post(self,request,msg_id):
        if 'unread' in request.POST:
            return self.change_status(msg_id)
        if 'delete' in request.POST:
            return self.delete_msg(msg_id)

    def delete_msg(self,msg_id):
        Message.objects.get(id=msg_id).delete()
        return redirect('doctor_messages')
    
    def change_status(self, msg_id):
        message = Message.objects.get(id=msg_id)
        message.readed = not message.readed
        message.save()
        return redirect('doctor_messages')
    
method_decorator(staff_member_required,name='dispatch')
class PerscriptionCreate(View):
    def get(self,request):
        if request.user.is_staff:
            patients = Patient.objects.all()

            if 'firstname' in request.GET:
                patients = self.get_patient_firstname
            elif 'lastname' in request.GET:
                patients = self.get_patient_lastname
            elif 'clear' in request.GET:
                return redirect('doctor_perscription')
        
            context = {'patients':patients}
            return render(request,'main/perscription_create.html',context)
        else:
            return HttpResponse('Only for staff members')
    
    
    def get_patient_firstname(self):
        data = self.request.GET.get('firstname')
        print(data)
        patients = Patient.objects.filter(firstname__contains=data)
        return patients

    
    def get_patient_lastname(self):
        data = self.request.GET.get('lastname')
        patients = Patient.objects.filter(lastname__contains=data)
        return patients
    
method_decorator(staff_member_required,name='dispatch')
class PerscriptionCreateForm(View):
    def get(self,request,user_id):
        if 'medicine_query' in request.GET:
            query = request.GET.get('medicine_query')
            medicines = self.get_med_query(query)
        elif 'clear' in request.GET:
            return redirect('perscription_create',user_id)
        else:
            medicines = Medicine.objects.all()
        context = {'medicines':medicines}
        return render(request,'main/perscription_form.html',context)

    def post(self,request,user_id):
        patient = Patient.objects.get(id=user_id)
        if 'medicine_id' in request.POST:
            med_id = request.POST.get('medicine_id')
            self.create_perscription_item(patient,med_id)
        if 'create_perscription' in request.POST:
            perscription = self.get_perscription(patient)
            perscription.status = True
            perscription.save()
            return redirect('dashboard')
        return redirect('perscription_create',user_id)
    
    def create_perscription_item(self,patient,item_id):
        item_id = self.request.POST.get('medicine_id')
        perscription = self.get_perscription(patient)
        PerscriptionItems.objects.create(perscription=perscription,medicine = Medicine.objects.get(id=item_id))

    def get_perscription(self,patient):
        perscription,created = Perscription.objects.get_or_create(patient=patient,doctor=Doctor.objects.get(user=self.request.user),status=False)
        return perscription
    
    def get_med_query(self,query):
        medicines = Medicine.objects.filter(name__contains=query)
        return medicines

method_decorator(staff_member_required,name='dispatch')
class MeetingsPage(View):
    def get(self,request):
        if request.user.is_staff:
            context = {}
            return render(request,'main/meetings_create.html',context)
        else:
            return HttpResponse('Only for staff members')
        
class DoctorLoginPage(View):
    def get(self,request):
        form = DoctorUserLoginForm()
        context = {'login_form':form}
        return render(request,'main/doctor_login_page.html',context)
    
    def post(self,request):
        form = DoctorUserLoginForm(request,data=request.POST)
        return  self.form_validation(form,'dashboard')
    
    def form_validation(self,form,succes_url):
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_staff:
                login(self.request,user)
                return redirect(succes_url)
            else:
                return HttpResponse('Invalid data try again later')
        else:
            return HttpResponse('Invalid data try again later')

class DoctorRegisterPage(View):
    def get(self, request):
        form = DoctorRegisterForm()
        context = {'register_form': form}
        return render(request, 'main/doctor_register_page.html', context)

    def post(self, request):
        form = DoctorRegisterForm(request.POST)
        return self.form_validation(form, 'doctor_login_page')

    def form_validation(self, form, success_url):
        if form.is_valid():
            user = form.save()
            Doctor.objects.create(
                user=user,
                firstname=user.first_name,
                lastname=user.last_name,
                email=user.email,
            )
            return redirect(success_url)
        else:
            return HttpResponse('Invalid data. Please try again later.')
        
method_decorator(staff_member_required,name='dispatch')
class DoctorLogout(View):
    def get(self,request):
        logout(request)
        return redirect('doctor_login_page')
    

