from django import forms
from django.forms import ModelForm,TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from main.models import Patient,Doctor,Apointment,Medicine,Perscription,Meeting,Room,Message


class MessageForm(ModelForm):
    def __init__(self,*args,**kwargs ):
        super().__init__(*args,**kwargs)
        self.fields['reciver'].widget.attrs.update({
            'required':'',
            'name':'reciver',
            'id':'reciver',
            'class':'form-control',
            'placeholder':'Choose a reciver'
        })
        self.fields['title'].widget.attrs.update({
            'required':'',
            'name':'title_form',
            'id':'title_form',
            'class':'form-control',
            'placeholder':'Title'
        })
        self.fields['body'].widget.attrs.update({
            'required':'',
            'name':'body',
            'id':'body',
            'type':'text',
            'class':'form-control',
            'placeholder':'Write a message',
        })
        
    class Meta:
        model = Message 
        fields = ('title','reciver','body')
        labels = {
            'title':'Message title',
            'reciver' : 'Reciver',
            'body':'Message',
        }

class DoctorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'class':'form-control',
            'placeholder':'Username'
        })
        self.fields['first_name'].widget.attrs.update({
            'required':'',
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'class':'form-control',
            'placeholder':'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'required':'',
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'class':'form-control',
            'placeholder':'Last Name'
        })
        self.fields['email'].widget.attrs.update({
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'class':'form-control',
            'placeholder':'E-Mail'
        })
        self.fields['password1'].widget.attrs.update({
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'class':'form-control',
            'placeholder':'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'class':'form-control',
            'placeholder':'Retype password'
        })

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        
    def save(self,commit=True):
        user = super(DoctorRegisterForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True
        if commit:
            user.save()
        return user
    
class DoctorUserLoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'class':'form-control',
            'placeholder':'Username'
        })
        self.fields['password'].widget.attrs.update({
            'required':'',
            'name':'password',
            'id':'password',
            'type':'password',
            'class':'form-control',
            'placeholder':'Password'
        })
