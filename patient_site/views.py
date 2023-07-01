from django.shortcuts import render,redirect
from django.views import View
from main.models import Patient,Apointment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
        apointments = Apointment.objects.filter(patient=patient)
        context = {'apointments':apointments,'patient':patient}
        return render(request,'patient_page/home_log.html',context)
    
    def post(self,request):
        if 'delete' in request.POST:
            Apointment.objects.get(id=request.POST.get('delete')).delete()
        return redirect('home_page_logged')