from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from . import form
from .form import LoginForm
from .form import CustomRegisterForm

# Create your views here.

def registration(request):
    if request.method == 'POST':
        Form = CustomRegisterForm(request.POST)
        if Form.is_valid():
            messages.success(request,'Konto założone')
            user = Form.save()
            profil = models.Profil.objects.create(User=user,Opis='Tymczasowy Opis')
            profil.save()
            return redirect('home')
        else:
            messages.error(request,"Błąd")
            return render(request,'Blog/registration.html',{'form': Form})
    else:
        Form = CustomRegisterForm()
        return render(request,'Blog/registration.html',{'form': Form})

def home(request):
    posts = models.Post.objects.all()
    return render(request,"Blog/main.html",{'posts': posts})
def login(request):
    if request.user.is_authenticated():
        messages.success(request,'Zalogowano')
        return render(request,"Blog/main.html")
    else:
        return render(request,"Blog/main.html")