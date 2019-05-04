from django.shortcuts import render
from django.contrib import messages
from . import models
from . import form
from .form import LoginForm,RegisterForm
# Create your views here.

def registration(request):
    if request.method == 'POST':
        Form = RegisterForm(request.POST)
        if Form.is_valid():
            messages.success(request,"Konto założone")
            user = Form.save()
            profil = models.Profil(User=user)
            profil.save()
            return redirect('home')
        else:
            messages.error(request,"Błąd")
            return render(request,'Blog/registration.html',{'form': Form})
    else:
        Form = RegisterForm()
        return render(request,'Blog/registration.html',{'form': Form})