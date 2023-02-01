from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from api.models import ToDosn

class UserRegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]        

         #styling model form
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"foem-control"}),
            
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))     



class TodoForm(forms.ModelForm):
    class Meta:
        model=ToDosn
        fields=["Task_name"]       

        widgets={
            "Task_name":forms.TextInput(attrs={"class":"form-control"})
        }