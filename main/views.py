from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.contrib.auth import logout,login,authenticate
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from main.models import Patient,Doctor,Apointment,Medicine,Perscription,Meeting,Room
from .forms import MessageForm,DoctorRegisterForm,DoctorUserLoginForm

method_decorator(staff_member_required,name='dispatch')
class DashboardPage(View):
    def get(self,request):
        if request.user.is_staff:
            doctor = Doctor.objects.get(user=request.user)
            form = MessageForm()

            apointments = Apointment.objects.filter(doctor=doctor).order_by('date')
            apointments_list = self.check_dates(apointments)

            meetings = Meeting.objects.filter(doctors=doctor).order_by('date')
            meetings_list = self.check_dates(meetings)
            context = {'apointments':apointments_list,
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
        Apointment.objects.get(id=appointment_id).delete()
        return redirect('dashboard')
    
    def post_confirm_appointment(self):
        appointment_id = self.request.POST.get('confirm')
        appointment = Apointment.objects.get(id=appointment_id)
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
    def get(self,request):
        if request.user.is_staff:
            context = {}
            return render(request,'main/doctor_calendar.html',context)
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
                phone_number='000000000'
            )
            return redirect(success_url)
        else:
            return HttpResponse('Invalid data. Please try again later.')
        
method_decorator(staff_member_required,name='dispatch')
class DoctorLogout(View):
    def get(self,request):
        logout(request)
        return redirect('doctor_login_page')
    

