from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil
class LoginForm(forms.Form):
    UserName= forms.CharField(max_length=150)
    password= forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2','email') 
    
    def clean_Password(self):
        password1= self.data.get('Password')
        password2 = self.data.get('RepeatPassword')
        if  password1 != password2:
           raise forms.ValidationError("Passwords are not similar")
        return self.cleaned_data.get('Password')

class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['Zdjecie']